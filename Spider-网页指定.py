import urllib.parse
from urllib import parse,request


ul='http://www.baidu.com/s?'

url=[ul+parse.urlencode({'wd':'赵丽颖','pn':i}) for i in range(0,60,10)]
for item in url:
    print(item)




