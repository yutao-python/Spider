from selenium import webdriver
import time

import pymongo

# ele.send_keys('')
class JD:
    def __init__(self):
        self.url='https://www.jd.com/'
        #无头模式
        # self.option=webdriver.FirefoxOptions()
        # self.option.add_argument('--headless')
        # self.browser = webdriver.Firefox(options=self.option)

        self.browser = webdriver.Firefox()
        self.browser.get(url=self.url)
        #mongodb相关变量
        # self.conn=pymongo.MongoClient('loaclhost',27017)
        # self.db=self.conn['jddb']
        # self.myset=self.conn['jdset']

    def get_html(self):
        # 搜索框//*[@id="key"]
        self.browser.find_element_by_xpath('//*[@id="key"]').send_keys('爬虫书')
        #点击按钮 //*[@id="search"]/div/div[2]/button
        self.browser.find_element_by_xpath('//*[@id="search"]/div/div[2]/button').click()
        #添加等待时间,等待页面加载
        time.sleep(2)

    def get_one_page(self):
        #当前页面下拉到底[实现页面动态全加载]
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        time.sleep(2)
        #抓取多条数据
        li_list = self.browser.find_elements_by_xpath('//*[@id="J_goodsList"]/ul/li')

        for li in li_list:
            item = {}
            try:
                item['price'] = li.find_element_by_xpath('.//div[@class="p-price"]').text
                item['mame'] = li.find_element_by_xpath('.//div[@class="p-name"]/a/em').text
                item['commit'] = li.find_element_by_xpath('.//div[@class="p-commit"]/strong').text
                item['shop'] = li.find_element_by_xpath('.//div[@class="p-shopnum"]').text
                print(item)
                # 存入到mongodb
                # self.myset.insert(item)
            except Exception as  e:
                print(e)

    def run(self):
        self.get_html()
        while True:
            self.get_one_page()
            if self.browser.page_source.find('pn-next disabled')==-1:
                self.browser.find_element_by_xpath('//*[@id="J_bottomPage"]/span[1]/a[9]').click()
                time.sleep(1)
            else:
                self.browser.quit()
                break
if __name__ == '__main__':
    a=JD()
    a.run()