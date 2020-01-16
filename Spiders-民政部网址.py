from selenium import webdriver
import time
class MZ:
    def __init__(self):
        self.url='http://www.mca.gov.cn/article/sj/xzqh/2019/'
        self.browser=webdriver.Firefox()
        self.browser.get(url=self.url)

    def parser_html(self):
        self.browser.find_element_by_xpath('//*[@id="list_content"]/div[2]/div/ul/table/tbody/tr[2]/td[2]/a').click()
        # //*[@id="list_content"]/div[2]/div/ul/table/tbody/tr[2]/td[2]/a
        #切换页面窗口
        ##获取当前所有窗口
        time.sleep(2)
        all=self.browser.window_handles
        ##切换browser到当前所有窗口的指定位置[使用索引]
        self.browser.switch_to.window(all[1])
        time.sleep(3)
        self.get_one_html()
    def get_one_html(self):
        #获取当前指定的页面[//*[@id="2019年11月份县以上行政区划代码_28029"]/table/tbody/tr[@height="19"]]
        r_list=self.browser.find_elements_by_xpath('//*[@id="2019年11月份县以上行政区划代码_28029"]/table/tbody/tr[@height="19"]')
        for tr in r_list:
            code = tr.find_element_by_xpath('./td[2]').text.strip()
            name = tr.find_element_by_xpath('./td[3]').text.strip()
            print(name, code)

    #启动函数
    def run(self):
        self.parser_html()

if __name__ == '__main__':
    a=MZ()
    a.run()