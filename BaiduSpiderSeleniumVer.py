import re
import threading
import time
from pprint import pprint
import traceback
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # 用于键盘操作
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from util import log

errorNum = 0
year = 2014

src_filename = f"./occurrenceFile/{year}_occurrence.csv"
target_filename = f"./result/{year}_baidu_result_selenium_version.csv"
target_temp_filename_format = "./temp/selenium/"+str(year)+"_baidu_result_temp_{}.csv"

log_filename = f"./log/{year}_baidu_result_selenium_version"  # 这里不加.log

logger = log.LogFactory(log_filename).getLogger()

class Spider:
    def __init__(self, url):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.page_load_strategy = "none"

        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")
        # self.browser.implicitly_wait(5)  # 隐式等待
        self.baseUrl = url
        self.startTimestamp = 0
        self.endTimestamp = 0
        self.startTime = ""
        self.endTime = ""
        self.startTimeFormat = "{}-01-01 00:00:00"
        self.endTimeFormat = "{}-12-31 23:59:59"
        self.setTime(2000)  # 默认年份

        self.browser.get(url)
        self.wait = WebDriverWait(self.browser, 3)

    def setTime(self, year):
        self.startTime = self.startTimeFormat.format(year)
        self.endTime = self.endTimeFormat.format(year)
        self.startTimestamp = self.timeStringToTimestamp(self.startTime)
        self.endTimestamp = self.timeStringToTimestamp(self.endTime)

    def timeStringToTimestamp(self, string):
        timeArray = time.strptime(string, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp

    def runV2(self, Id, keyword):
        while True:
            try:
                # 整个页面加载完成
                self.browser.get(self.baseUrl)
                # target_url = self.baseUrl + f's?wd={keyword}' + f'&gpc=stf%{self.startTimestamp}%2C{self.endTimestamp}%7Cstftype%3D2'

                # 输入搜索内容并点击"百度一下"
                inputForm = WebDriverWait(self.browser, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="kw"]')), message='百度页面加载超时')
                # inputForm.clear()  # 先清空内容
                inputForm.send_keys(keyword)
                inputForm.send_keys(Keys.ENTER)

                # 构造新的目标url，用于限定时间
                # WebDriverWait(self.browser, 3).until(lambda driver: driver.execute_script('return document.readyState') == 'complete',message="百度页面更新超时")
                # 用这个方式限制时间是否会更快?
                target_url = self.browser.current_url + f'&gpc=stf%{self.startTimestamp}%2C{self.endTimestamp}%7Cstftype%3D2'
                self.browser.get(target_url)

                #处理结果数量
                #todo 可能存在一个问题：resultElement可能没有加载出来，NoneType has not attribute 'text'
                #还是存在问题：得到的结果还是原来页面中的信息
                # self.browser.refresh()  #通过refresh是否能解决？
                time.sleep(0.5)

                WebDriverWait(self.browser, 3).until(lambda driver: driver.execute_script('return document.readyState') == 'complete',message="新页面更新超时")
                soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                resultElement = soup.find('span', {"class": "hint_PIwZX c_font_2AD7M"})
                ret = re.search('[1-9]\d*|0', resultElement.text)
                return ret.group()

            except NoSuchElementException as e:
                logger.error(f"id:{Id}, detail:{e.args[0]}")
                pprint(f"id:{Id}, detail:{e.args[0]}")
            except TimeoutException as e:
                logger.error(f"id:{Id}, detail:{e.args[0]}")
                pprint(f"id:{Id}, detail:{e.args[0]}")
            except Exception as e:
                # logger.exception(e)
                logger.error(f"id:{Id}, detail:\n{traceback.format_exc()}")
                pprint(f"id:{Id}, detail:\n{traceback.format_exc()}")

    def run(self, Id, keyword):
        global logger
        while True:
            try:
                # 整个页面加载完成
                self.browser.get(self.baseUrl)
                self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

                # 输入搜索内容并点击"百度一下"
                inputForm = self.browser.find_element(By.XPATH, '//*[@id="kw"]')
                inputForm.clear()  # 先清空内容
                inputForm.send_keys(keyword)
                inputForm.send_keys(Keys.ENTER)
                # submitButton = self.browser.find_element(By.XPATH, '//*[@id="su"]')
                # submitButton.click()

                # 修改时间
                # 1.点击展开时间选择

                # 整个页面加载完成
                self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                # todo 这里容易超时，不知道原因
                timeRit = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="timeRlt"]')), message="时间选择窗口未加载")
                timeRit.click()

                start = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="custom_2wanX"]/div[2]/div[1]/input')), message="开始时间未加载")
                start.click(), start.clear()
                start.send_keys(self.startTime)
                start.send_keys(Keys.ENTER)

                end = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="custom_2wanX"]/div[3]/div[1]/input')), message="结束时间未加载")
                end.click(), end.clear()
                end.send_keys(self.endTime)
                start.send_keys(Keys.ENTER)

                confirmButton = self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="custom_2wanX"]/div/button')), message="确定按钮未加载")
                confirmButton.click()

                # 因为页面中没有，只能把html代码搞出来
                # self.wait.until(
                #     EC.visibility_of_element_located((By.XPATH, '//span[@class="hint_PIwZX c_font_2AD7M"]')), "结果未加载成功")
                # resultElement = self.browser.find_element(By.XPATH, '//span[@class="hint_PIwZX c_font_2AD7M"]')
                # print(resultElement.text)

                # 整个页面加载完成
                # self.wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
                self.wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(0.5)  # todo 等待新加载的页面，否则会拿到原本没设置时间的数值，暂时用sleep解决
                soup = BeautifulSoup(self.browser.page_source, 'html.parser')
                resultElement = soup.find('span', {"class": "hint_PIwZX c_font_2AD7M"})
                ret = re.search('[1-9]\d*|0', resultElement.text)
                # print(ret.group())
                return ret.group()

            except NoSuchElementException as e:
                logger.error(f"id:{Id}, detail:{e.args[0]}")
                # pprint(e)
                # print("未找到元素")
                # time.sleep(1)
                # self.browser.refresh()
            except TimeoutException as e:
                logger.error(f"id:{Id}, detail:{e.args[0]}")
                # pprint(e)
                # print("**超出时间限制**")
                # self.browser.refresh()
            except Exception as e:
                # logger.exception(e)
                logger.error(f"id:{Id}, detail:\n{traceback.format_exc()}")
                # pprint(e)
                # self.browser.refresh()


def thread_func(id_list, address_list, i):
    spider = Spider("https://www.baidu.com/")
    spider.setTime(year)  # 设置年份
    with open(target_temp_filename_format.format(i), "w") as f:
        for Id, address in zip(id_list, address_list):
            # get_connect(Id, address)

            resultNum = spider.runV2(Id, address)
            logger.info("[{}] Thread-{} | id:{} | address:{} | result:{}"
                  .format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), i, Id, address, resultNum))
            # print("[{}] Thread-{} | id:{} | address:{} | result:{}"
            #       .format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), i, Id, address, resultNum))
            f.write(f"{Id},{resultNum}\n")
            # time.sleep(1)

if __name__ == '__main__':
    df = pd.read_csv(src_filename)
    address_list = df['address']
    id_list = df['Id']
    # print(len(id_list))
    # n = round(len(address_list) / 5)
    # for i in range(5):
    # get_connect(id_list, address_list)
    # print(n * (i + 1))
    # t = threading.Thread(target=get_connect, args=(id_list[n * i:n * (n + 1)], address_list[n * i:n * (n + 1)], i,))
    # t.start()

    # spider = Spider("https://www.baidu.com/")
    # spider.setTime(2012)  # 设置年份
    #
    # for Id, address in zip(id_list, address_list):
    #     # get_connect(Id, address)
    #     resultNum = spider.run(address)
    #     print("id:{} | address:{} | result:{}".format(Id, address, resultNum))
    #     time.sleep(2)


    # 多线程方案
    # 开五个线程
    n = 8
    total = len(df)
    batch = total // n + 1

    threads = []
    for i in range(0,n):
        start = i * batch
        end = (i+1) * batch

        t = threading.Thread(target=thread_func, args=(id_list[start:end], address_list[start: end],i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # 将临时文件合并
    with open(target_filename, "w") as f:
        for i in range(0, n):
            with open(target_temp_filename_format.format(i), "r") as f1:
                f.write(f1.read())

    print("Error Times:{}".format(errorNum))
    print("Exit Main Thread")
