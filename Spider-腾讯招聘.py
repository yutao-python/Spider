"""
腾讯招聘指定信息抓取
"""
import requests
import json
from threading import Thread,Lock
from queue import Queue
from urllib import parse
from fake_useragent import UserAgent
import time

class TX:
    def __init__(self):
        self.one_url='https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1579072774464&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'

        self.two_url = 'https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1563912374645&postId={}&language=zh-cn'
        self.headers={'User-Agent':UserAgent().random}
        #创建2个线程,处理不同URL
        self.one_q=Queue()
        self.two_q=Queue()
        #存入json文件
        # self.f=open('腾讯招聘.json','w')
        #计数
        self.i=0
        #线程锁
        self.lock=Lock()

    def url_in(self):
        # word=input('输入职位:')
        word='爬虫'
        keyword = parse.quote(word)

        total = self.get_total(keyword)
        for page in range(1, total+1):
            one_url = self.one_url.format(keyword,page)
            self.one_q.put(one_url)
        # print(url)


    # 获取总页数
    def get_total(self, keyword):
        url = self.one_url.format(keyword, 1)
        html = requests.get(url=url, headers=self.headers).json()
        numbers = int(html['Data']['Count'])
        if numbers % 10 == 0:
            total = numbers // 10
        else:
            total = numbers // 10 + 1

        return total

    def get_html(self,url):
        html=requests.get(url=url,headers=self.headers).text
        return html
    #一级页面线程事件函数
    def one_get_html(self):
        while not self.one_q.empty():
            one_url=self.one_q.get()
            one_html=json.loads(self.get_html(one_url))
            # print(one_html)
            for item in one_html['Data']['Posts']:
                PostId=item['PostId']
                two_url=self.two_url.format(PostId)
                # print(two_url)
                self.two_q.put(two_url)
                # print('--------------')

    #二级页面
    def two_get_html(self):
        while not self.two_q.empty():
            two_url=self.two_q.get(block=True,timeout=3)
            # print(two_url)
            html=json.loads(self.get_html(two_url))
            item={}
            item['name'] = html['Data']['RecruitPostName']
            item['duty'] = html['Data']['Responsibility']
            item['require'] = html['Data']['Requirement']
            print(item)
            self.lock.acquire()
            self.i += 1
            self.lock.release()


    def run(self):
        self.url_in()
        l1_list=[]
        l2_list=[]
        for i in range(2):
            ti=Thread(target=self.one_get_html)
            l1_list.append(ti)
            ti.start()
        time.sleep(0.1)
        for j in range(2):
            t2=Thread(target=self.two_get_html)
            l2_list.append(t2)
            t2.start()

        for i in l1_list:
            i.join()
        for j in l2_list:
            j.join()
        print('总数量:',self.i)

if __name__ == '__main__':
    start_time=time.time()
    a=TX()
    a.run()
    end_time=time.time()
    print('执行时间:',end_time-start_time)

