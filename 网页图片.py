from urllib import request
import urllib
import re
def get_html(url):
    # url='https://maoyan.com/films'
    headers={'User-Agent':'Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13'}
    res=request.Request(url=url,headers=headers)
    resp=urllib.request.urlopen(res)
    html=resp.read()
    return html
def save_html(filename,html):
    f=open('./TP/'+filename,'wb')
    f.write(html)
    f.close()
a=open('图片.html','r')
html=a.read()
pattern = re.compile('<img data-src="(.*?jpg)@.*?"')
r_list=pattern.findall(html)
# print(r_list)
for url in r_list:
    print(url)
    html=get_html(url)
    url_list=url.split('/')
    filename=url_list[4]
    # print(type(filename))
    save_html(filename,html)
print('完成')

    # print(type(item))
# with open('图片.txt','w') as f:
#     for item in r_list:
#         f.write(item+'\n')
# f.close()
# a.close()
