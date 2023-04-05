import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # 用于键盘操作

import log
import test

import aiofiles  # pip install aiofiles

def testLog():
    logger = log.LogFactory("./log/test").getLogger()
    logger.info("123")
    logger.error("123")

def testSelenium():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = "eager"
    # chrome_options.add_argument('--headless')
    browser = webdriver.Chrome(options=chrome_options, executable_path="./chromedriver")
    browser.get("https://www.baidu.com/")
    # 输入搜索内容并点击"百度一下"
    inputForm = browser.find_element(By.XPATH, '//*[@id="kw"]')
    inputForm.clear()  # 先清空内容
    inputForm.send_keys('title:("赛格电子市场（华强北路）" "华强北")')
    inputForm.send_keys(Keys.ENTER)

    print(browser.current_url)
    target_url = browser.current_url + '&gpc=stf%3D1325347200%2C1356883200%7Cstftype%3D2'  # 用这个方式限制时间更快
    browser.get(target_url)
    print(browser.current_url)

async def testAio():
    x = ["!23",123,123,4321,4,213,1,4,124,21]
    print(datetime.datetime.now())
    async with aiofiles.open("testAio.txt", 'w') as fp:
        for y in x:
            await fp.write(y)
    print(datetime.datetime.now())


if __name__ == '__main__':
    # testLog()
    # testSelenium()
    testAio()
    pass


