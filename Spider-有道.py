    # data-dict:
    # salt: 15789645589091
    # sign: 3ff87cbfd0d896dc6e882b11cd8aa3a7
    # ts: 1578964558909
    # bv: 56e87615b96ab60016d8f1dbe4612d37
from urllib import parse

import requests
import time
import random
from hashlib import md5
from lxml import etree

class YdSpider:
    def __init__(self):
        self.post_url='http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        self.headers={
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Connection': 'keep-alive',
            # 'Content-Length': '251',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'OUTFOX_SEARCH_USER_ID=-229397829@10.169.0.84; OUTFOX_SEARCH_USER_ID_NCOO=1338384440.160748; _ntes_nnid=e2c9f689fabef6de2dba644d5ccb78e6,1575459625790; _ga=GA1.2.1687741542.1576112010; JSESSIONID=aaacbp3dzGLaV4Cl8MH_w; ___rl__test__cookies=1578966828463',
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }


    def get_ts_salt_sign(self,word):
        ts=str(int(time.time()*1000))
        salt=ts+str(random.randint(0,9))
        #sign是md5加密
        string='fanyideskweb'+word+salt+"n%A-rKaT5fb[Gy?;N5@Tj"
        s=md5()
        s.update(string.encode())
        sign=s.hexdigest()

        return ts,salt,sign

    def attack_yd(self,word):
        ts,salt,sign=self.get_ts_salt_sign(word)

        data={
            'i': word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'ts': ts,
            'bv': '56e87615b96ab60016d8f1dbe4612d37',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTlME',
        }
        # 3. 直接发请求:requests.post(url,data=data,headers=xxx)
        res = requests.post(
            url=self.post_url,
            data=data,
            headers=self.headers
        )
        # res.json() 将json格式的字符串转为python数据类型
        html = res.json()
        # html:{'translateResult': [[{'tgt': '你好', 'src': 'hello'}]], 'errorCode': 0, 'type': 'en2zh-CHS', 'smartResult': {'entries': ['', 'n. 表示问候， 惊奇或唤起注意时的用语\r\n', 'int. 喂；哈罗\r\n', 'n. (Hello)人名；(法)埃洛\r\n'], 'type': 1}}
        result = html['translateResult'][0][0]['tgt']
        print(result)
        url='https://image.baidu.com/search/index?tn=baiduimage&ie=utf-8&word={}'
        params = parse.quote(word)
        url = url.format(params)
        print(url)
        # 主函数

    def run(self):
        # 输入翻译单词
        while True:
            word = input('请输入要翻译的单词(退出请输入0):')
            if word=='0':
                break
            self.attack_yd(word)

if __name__ == '__main__':
    spider = YdSpider()
    spider.run()
