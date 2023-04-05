import re
import time
import traceback

from BaiduSpider import BaiduSpider
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # 用于键盘操作
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from config import logger


class BaiduSpiderSelenium(BaiduSpider):
    def __init__(self, url, startYear: int, endYear: int):
        BaiduSpider.__init__(self, url, startYear, endYear)

        # chrome浏览器设置
        chrome_options = webdriver.ChromeOptions()
        chrome_options.page_load_strategy = "none"

        desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
        desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')

        self.browser = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")
        self.wait = WebDriverWait(self.browser, 3)

    def run(self, Id, keyword) -> int:
        while True:
            try:
                # 整个页面加载完成
                self.browser.get(self.url)
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
                timeRit = self.wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="timeRlt"]')),
                                          message="时间选择窗口未加载")
                timeRit.click()

                start = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="custom_2wanX"]/div[2]/div[1]/input')),
                    message="开始时间未加载")
                start.click(), start.clear()
                start.send_keys(self.startTime)
                start.send_keys(Keys.ENTER)

                end = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="custom_2wanX"]/div[3]/div[1]/input')),
                    message="结束时间未加载")
                end.click(), end.clear()
                end.send_keys(self.endTime)
                start.send_keys(Keys.ENTER)

                confirmButton = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="custom_2wanX"]/div/button')),
                    message="确定按钮未加载")
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
                return int(ret.group())

            except NoSuchElementException as e:
                logger.error(f"id:{Id}, detail:{e.args[0]}")

            except TimeoutException as e:
                logger.error(f"id:{Id}, detail:{e.args[0]}")

            except Exception as e:
                logger.error(f"id:{Id}, detail:\n{traceback.format_exc()}")

