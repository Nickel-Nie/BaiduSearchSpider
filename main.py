import time
import pandas as pd

from util.log import MyLog
from util.threadUtil import ThreadUtil
from config import *
from spider.BaiduSpiderRequest import BaiduSpiderRequest

# 先调整config文件中的相关配置信息，再启动
def thread_func(id_list, address_list, i):
    spider = BaiduSpiderRequest("https://www.baidu.com/s", year, year)
    with open(target_temp_filename_format.format(i), "a+") as f:
        for Id, address in zip(id_list, address_list):
            resultNum = spider.run(Id, address)

            logger.info("[{}] Thread-{} | id:{} | address:{} | result:{}"
                  .format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), i, Id, address, resultNum))
            # print("[{}] Thread-{} | id:{} | address:{} | result:{}"
            #       .format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), i, Id, address, resultNum))
            f.write(f"{Id},{resultNum}\n")
            # time.sleep(1)

# 崩溃恢复，从./temp/{version}/temp_{i}.csv中读取上次崩溃的位置，然后继续爬取
# n表示线程数量，也即为临时文件的数量
"""
崩溃恢复的思路：
1. 首先读取src_filename对应的文件，得到address_list和id_list，从而确定爬取的总数量
2. 然后读取./temp/{version}/{year}_baidu_result_temp_{i}.csv文件，得到已经爬取的数量
3. 然后将address_list和id_list分别切片，得到剩余的address_list和id_list
"""
def crash_recovery(n:int, id_args:list, address_args:list):
    id_list = []
    address_list = []
    for i in range(0, n):
        id_arg = id_args[i]
        address_arg = address_args[i]
        with open(target_temp_filename_format.format(i), "r") as f1:
            lines = f1.readlines()
            # 删除lines中的空字符串
            lines = list(filter(lambda x: x != "\n", lines))
            # 读取到的最后一行
            last_line = lines[-1]
            # 读取到的最后一行的id
            last_id = last_line.split(",")[0]
            # 找到id_list中值为last_id的索引
            last_id_index = id_arg.index(last_id)
            # 切片
            id_arg = id_arg[last_id_index+1:]
            address_arg = address_arg[last_id_index+1:]
            id_list.append(id_arg)
            address_list.append(address_arg)
    
    return id_list, address_list



if __name__ == '__main__':
    df = pd.read_csv(src_filename)
    address_list = df['address']
    id_list = df['Id']

    # 启动日志守护进程
    logger.start()  # 异步写文件
    print(f"logger thread id: {logger.ident}")

    threadNum = 8

    # 第一次使用：
    # 将address_list和id_list平均切分为threadNum份。每个线程爬取一份
    total = len(address_list)
    step = total // threadNum + 1
    id_args = [id_list[i:i+step] for i in range(0, total, step)]
    address_args = [address_list[i:i+step] for i in range(0, total, step)]

    # 崩溃恢复使用：
    # id_args, address_args = crash_recovery(threadNum, id_args, address_args)


    # 创建线程并启动
    threadUtil = ThreadUtil(threadNum, thread_func, id_args, address_args)
    # 启动线程
    threadUtil.run()
    logger.stop()


    # 将生成的临时文件合并为最终结果
    with open(target_filename, "w") as f:
        for i in range(0, threadNum):
            with open(target_temp_filename_format.format(i), "r") as f1:
                f.write(f1.read())


