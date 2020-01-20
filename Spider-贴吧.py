from urllib import request,parse
from time import sleep
import random
import re
class TiebaSpider:
    def __init__(self):
        self.url='http://tieba.baidu.com/f?kw={}&ie=utf-8&tp=0&pn={}'
        self.headers = {'User-Agent':'Mozilla/5.0'}
    #请求
    # http://tieba.baidu.com/f?kw=%E6%B9%96%E5%8D%97%E5%A4%A7%E5%AD%A6&ie=utf-8&tp=0&pn=0
    #解析
    def get_html(self,url):
        req=request.Request(url=url,headers=self.headers)
        resp=request.urlopen(req)
        html=resp.read().decode()
        return html
    #保存
    def save_html(self,filename,html):
        with open(filename,'w') as f:
            # img_list=re.findall('img.*/$',html,re.S)
            # for imag in img_list:
            f.write(html)
            f.close()
    #入口函数
    def run(self):
        tiebaname=input('贴吧名：')
        begin_index=int(input('开始页：'))
        end_index=int(input("结束页："))
        for item in range(begin_index-1,end_index):
            kw=parse.quote(tiebaname)
            pn=str(item*50)
            url=self.url.format(kw,pn)
            html=self.get_html(url)
            sleep(random.randint(1,2))
            filename='%s_第%d页.html'%(tiebaname,item+1)
            self.save_html(filename,html)
        print('ok')

if __name__ == '__main__':
    spider=TiebaSpider()
    spider.run()