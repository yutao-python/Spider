from urllib import request
import re
import time
import random
import pymysql
from hashlib import md5
import sys
import redis


class CarSpider(object):
    def __init__(self):
        self.url = 'https://www.che168.com/beijing/a0_0msdgscncgpi1lto1csp{}exx0/'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
        # self.db = pymysql.connect('localhost', 'root', 'attack', 'cardb', charset='utf8')
        self.db = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='cardb',
            charset='utf8'
        )
        self.cursor = self.db.cursor()
        # 连接redis去重
        self.r = redis.Redis(host='localhost', port=6379, db=0,password=123456)

    # 功能函数1 - 获取响应内容
    def get_html(self, url):
        req = request.Request(url=url, headers=self.headers)
        res = request.urlopen(req)
        html = res.read().decode('gb2312', 'ignore')

        return html

    # 功能函数2 - 正则解析
    def re_func(self, regex, html):
        pattern = re.compile(regex, re.S)
        r_list = pattern.findall(html)

        return r_list

    # 爬虫函数开始
    def parse_html(self, one_url):
        one_html = self.get_html(one_url)
        one_regex = '<li class="cards-li list-photo-li".*?<a href="(.*?)".*?</li>'
        href_list = self.re_func(one_regex, one_html)
        for href in href_list:
            # 加密指纹
            s = md5()
            s.update(href.encode())
            finger = s.hexdigest()
            # 如果指纹表中不存在[使用在redis中创建集合，利用集合的去重性来检查是否爬过]
            if self.r.sadd('car:urls', finger):#如果集合中存在，则添加失败
                # 每便利一个汽车信息，必须要把此辆汽车所有数据提取完成后再提取下一辆汽车信息
                url = 'https://www.che168.com' + href

                # 获取一辆汽车的信息
                self.get_data(url)
                time.sleep(random.randint(1, 2))
            else:
                sys.exit('抓取结束')

    # 获取一辆汽车信息
    def get_data(self, url):
        two_html = self.get_html(url)
        two_regex = '<div class="car-box">.*?<h3 class="car-brand-name">(.*?)</h3>.*?<ul class="brand-unit-item fn-clear">.*?<li>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<h4>(.*?)</h4>.*?<span class="price" id="overlayPrice">￥(.*?)<b'
        item = {}
        car_info_list = self.re_func(two_regex, two_html)
        item['name'] = car_info_list[0][0]
        item['km'] = car_info_list[0][1]
        item['year'] = car_info_list[0][2]
        item['type'] = car_info_list[0][3].split('/')[0]
        item['displacement'] = car_info_list[0][3].split('/')[1]
        item['city'] = car_info_list[0][4]
        item['price'] = car_info_list[0][5]
        print(item)

        one_car_list = [
            item['name'],
            item['km'],
            item['year'],
            item['type'],
            item['displacement'],
            item['city'],
            item['price']
        ]
        ins = 'insert into cartab values(%s,%s,%s,%s,%s,%s,%s)'
        self.cursor.execute(ins, one_car_list)
        self.db.commit()

    def run(self):
        for p in range(1, 2):
            url = self.url.format(p)
            self.parse_html(url)

        # 断开数据库链接
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    spider = CarSpider()
    spider.run()