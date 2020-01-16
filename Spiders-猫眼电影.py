from selenium import webdriver
import time

#无界面浏览器设置
# options=webdriver.FirefoxOptions()
# options.add_argument('--headless')


url = 'https://maoyan.com/board/4'
# browser=webdriver.Firefox(options=options)
browser=webdriver.Firefox()
browser.get(url)

def get_data():
    # 基准xpath: [<selenium xxx li at xxx>,<selenium xxx li at>]
    li_list = browser.find_elements_by_xpath('//*[@id="app"]/div/div/div[1]/dl/dd')
    item={}
    for dd in li_list:
        info_list = dd.text.split('\n')
        item['number'] = info_list[0]
        item['name'] = info_list[1]
        item['star'] = info_list[2]
        item['time'] = info_list[3]
        item['score'] = info_list[4]
        print(item)
# //*[@id="app"]/div/div/div[1]/dl/dd
get_data()
while True:
  get_data()
  try:
      browser.find_element_by_link_text('下一页').click()
      time.sleep(2)
  except Exception as e:
      print('恭喜你!抓取结束')
      browser.quit()
      break