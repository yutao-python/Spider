import csv
from urllib import request
import urllib
import re
import pymysql
import pymongo
from lxml import etree
# >db = pymysql.connect(参数列表)
# >>host ：主机地址,本地 localhost
# >>port ：端口号,默认3306
# >>user ：用户名
# >>password ：密码
# >>database ：库
# >>charset ：编码方式,推荐使用 utf8
db=pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='maoyan',
    charset='utf8'
)
cur=db.cursor()
class DianY:
    # 常用变量
    def __init__(self):
        # https: // maoyan.com / films?offset = 30
        # https: // maoyan.com / board
        self.url='https://maoyan.com/board'
        self.headers={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        self.conn = pymongo.MongoClient(host='192.168.153.137', port=27017)

    #请求
    def get_html(self):
        req=request.Request(url=self.url,headers=self.headers)
        resp=request.urlopen(req)
        html=resp.read().decode()
        return html

    def set_html_list(self,html):
        ##正则解析
        #创建正则
        # r = re.compile('<div class="movie-item-info">.*?title="(.*?)" data-act=.*?<p class="star">(.*?)</p>.*?<p class="releasetime">(.*?)</p>.*?</div>',re.S)
        #根据正则获取响应内容
        # r_list = r.findall(html)
        # l=[]
        # for item in r_list:
        #     l.append((item[0].strip(),item[1].strip()[3:],item[2].strip()[5:]))
        # # print(r_list)
        # return l
        ##xpath解析
        #创建xpath对象
        p=etree.HTML(html)
        #基于xpath获取响应内容--->节点对象列表
        x_list=p.xpath('//dl[@class="board-wrapper"]/dd')
        for dd in x_list:
            item={}
            item['name']=dd.xpath('.//p[@class="name"]/a/text()')[0].strip()
            item['star']=dd.xpath('.//p[@class="star"]/text()')[0].strip()[3:]
            item['time']=dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()[5:]
            print(item)
    def set_mysql(self,l):
        sql = 'insert into dianying values(%s,%s,%s)'
        cur.executemany(sql, l)
        db.commit()

    def set_csv(self,l):
        print(l)
        with open('dianying.csv','w')as f:
            writer=csv.writer(f)
            writer.writerows(l)

    def run(self):
        html= self.get_html()
        r_list=self.set_html_list(html)
        # self.set_mysql(r_list)
        # self.set_csv(r_list)
        print('完成')
        # begin_index=int(input('开始页数：'))
        # end_index=int(input('结束页数：'))
        # for i in range(begin_index-1,end_index):
        #     number=i*30
        #     url_number=self.url.format(number)

if __name__ == '__main__':
    movie=DianY()
    movie.run()

cur.close()
db.close()





