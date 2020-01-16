# http://app.mi.com/categotyAllListApi?page={}&categoryId=2&pageSize=30
import requests
import json
from threading import Thread,Lock
from queue import Queue
from fake_useragent import UserAgent

import csv
import time
import random
import re


class XM:
    def __init__(self):
        self.url='http://app.mi.com/categotyAllListApi?page={}&categoryId=1&pageSize=30'
        self.headers={'User-Agent':UserAgent().random}
        self.count=0
        #创建一个队列
        self.q=Queue()
        #创建一个线程锁
        self.l=Lock()
        self.f = open('xiaomi.csv','a',newline='')
        self.writer = csv.writer(self.f)


    def get_app_id(self):
        url='http://app.mi.com/'
        html=self.get_html(url)
        regex='<a href="/category(.*?)"'
        pattren=re.compile(regex,re.S)
        id_list=pattren.findall(html)
        for i in id_list:
            one_id=i
            return one_id

    def get_html(self,url):
        html_json=requests.get(url=url,headers=self.headers).text
        try:
            html=json.loads(html_json)
            return html
        except Exception as e:
            print(e)


    def url_put(self):
        i=self.get_int()
        for page in range(int(i)):
            url=self.url.format(page)
            self.q.put(url)

    def get_int(self):
        url=self.url.format(0)
        count=self.get_html(url)['count']
        i=count//30
        if count%30=='0':
            return i
        return i+1

    #主体函数,从队列中取出URL
    def url_get_html(self):
        while not self.q.empty():
            time.sleep(0.1)
            url=self.q.get()
            app_list=[]
            html=self.get_html(url)
            item={}
            for one_app in html['data']:
                item['app_name']=one_app['displayName']
                item['app_type']=one_app['level1CategoryName']
                item['one_url']=one_app['packageName']
                print(item)
                app_list.append((item['app_name'],item['app_type'],item['one_url']))
                self.l.acquire()
                self.count+=1
                self.l.release()
            self.l.acquire()
            self.writer.writerows(app_list)
            self.l.release()



    def run(self):
        self.url_put()
        t_list=[]
        for i in range(3):
            #创建线程
            t=Thread(target=self.url_get_html)
            t_list.append(t)
            t.start()
        #等待线程运行结束,统一回收线程
        for j in t_list:
            j.join()
        self.f.close()
        print('应用数量', self.count)




if __name__ == '__main__':
    s_time=time.time()
    a=XM()
    a.run()
    end_time=time.time()
    print(end_time-s_time)
# data: [
# {
# appId: 774623,
# displayName: "正宗漂流瓶",
# icon: "http://file.market.xiaomi.com/thumbnail/PNG/l62/AppStore/086d644eab89f43540c6784fc8681aa1deec2180b",
# level1CategoryName: "聊天社交",
# packageName: "com.bottlecp"
# },