import time
import pandas as pd

from util.log import MyLog
from util.threadUtil import ThreadUtil
from config import *
from spider.BaiduSpiderRequest import BaiduSpiderRequest

# 先调整config文件中的相关配置信息，再启动
def thread_func(id_list, address_list, i):
    spider = BaiduSpiderRequest("https://www.baidu.com/s", year, year)
    with open(target_temp_filename_format.format(i), "w") as f:
        for Id, address in zip(id_list, address_list):
            resultNum = spider.run(Id, address)

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

    # 启动日志守护进程
    logger.start()  # 异步写文件
    print(f"logger thread id: {logger.ident}")

    threadNum = 8
    threadUtil = ThreadUtil(threadNum, thread_func, [id_list, address_list])
    # 启动线程
    threadUtil.run()
    logger.stop()


    # 将生成的临时文件合并为最终结果
    with open(target_filename, "w") as f:
        for i in range(0, threadNum):
            with open(target_temp_filename_format.format(i), "r") as f1:
                f.write(f1.read())


