import re
import threading

from baiduspider import BaiduSpider
from pprint import pprint
from lxml import etree
from datetime import datetime
import pandas as pd
import time
import requests
from typing import List

src_filename = "../occurrenceFile/_2012_occurrence.csv"
target_filename = "../2012_baidu_result.csv"
target_temp_filename_format = "./temp/2012_baidu_result_temp_{}.csv"

# 会被ban
def init():
    # 百度更新TLS指纹识别验证机制的解决方法。
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'AES128'
    try:
        requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'AES128'
    except AttributeError:
        # no pyopenssl support used / needed / available
        pass

def write_result(f, resultList):
    for result in resultList:
        f.write(result)


def thread_func(id_list, address_list, i):
    spider = BaiduSpider(cookie='__yjs_duid=1_96e3b03f9ef1f6612ed87458ccae26ae1634350185465; PSTM=1634831082; BIDUPSID=7C65D7A96B67FF398F5FC73A66381915; BDUSS=5WN1VFdmNpVTl6ODBYR2xDYnMwZ0UwNUVsZFJ2VDFlMW9FMFZzQ245LVJDTGhoRVFBQUFBJCQAAAAAAAAAAAEAAADgj2NFc2gxdNi8OTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJF7kGGRe5BhZ3; BDUSS_BFESS=5WN1VFdmNpVTl6ODBYR2xDYnMwZ0UwNUVsZFJ2VDFlMW9FMFZzQ245LVJDTGhoRVFBQUFBJCQAAAAAAAAAAAEAAADgj2NFc2gxdNi8OTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJF7kGGRe5BhZ3; BAIDUID=E9E59FEF052D0913D8D9D6A08561AD88:FG=1; ZFY=4oaV07YWlw79Pjvo4XQVi8YSaamZOrfmq1e3jzAjTw8:C; BAIDUID_BFESS=E9E59FEF052D0913D8D9D6A08561AD88:FG=1; __bid_n=1845cfd4722b901e3c4207; FEID=v10-9577a6465b4f61726acfc0101140bcc8c812dd5a; BAIDU_WISE_UID=wapp_1672407124349_915; __xaf_fpstarttimer__=1672722114929; __xaf_thstime__=1672722115175; __xaf_fptokentimer__=1672722115206; FPTOKEN=UwMUhLChmd1afuyTYpd7m9KrqzFu1uLSmM+Xl+mLYs2Uc1FoPGGB6FDwzzU0CYnz1wCgR0GyVf7rgEQGNqwGHKnTVeIqwLw16B/Jx5F17EX7Tbn6tZ38F788IhQMsaSeTd4WhGgCgeIoXQrXbM8wdN+X+wpMnG8iF7ZdEJB8fWNnclOL4TQq1NUWQ3g3AorwX26O2vDr8FjzEi7dHArfR4ht57dO5fjtQoqkIcz1dXMXwAu3OkjcoZeffvy2eycGH9OmZOj9Qvq9iQ8GMKdh7wPiRI1tQki0LE49UjeqJIp3VwPU82EDaZv4GxJV74eniO+pEWJcDmPywcn1FEvg1Xu6Gf5NmFakURVTFYfLVFgYqv3tCsrcEBip33Z30DZB5UCU517GnNVs+7ZJFR7uOg==|sDFxbwpnxc/isvr5yK4rT4NVDjpQbI9tZ1h8dLTg9cw=|10|cfc3331abab6146e5a8fe12e48a02de6; RT="sl=1&ss=lfv7m1li&tt=1qp&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&z=1&dm=baidu.com&si=d80d4fc4-d23d-4043-8cc6-6f7a284b75eb&ld=2ir&ul=4dh&hd=4k2"; BD_UPN=12314753; BA_HECTOR=8k8h04ahaga0a40l25a00k0t1i2d0n81n; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BD_HOME=1; BD_CK_SAM=1; PSINO=1; delPer=0; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; sugstore=0; H_PS_PSSID=38185_36556_38407_38113_38470_38349_38440_38303_38468_38289_38380_37932_38356_26350_38420_38281_37881; baikeVisitId=3e5a16b3-a3be-4ec3-8b28-da9e63da4fb2; H_PS_645EC=20cfZkeLAluXD%2F%2F8ebTj1zZjxJIGAw36GTpOkH6RrLQ%2F8PHJlqXqnOuB7V5db96Hk2Ez')

    resultList = []
    curNum = 0

    with open(target_temp_filename_format.format(i), "w") as f:
        for Id, address in zip(id_list, address_list):
            while True:
                try:
                    # resultNum = spider.search_web(query=address, time=(datetime(2012, 1, 1), datetime(2012, 12, 31))).total
                    # print("[{}] Thread-{} | id:{} | address:{} | result:{}"
                    #       .format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), i, Id, address,
                    #               resultNum))

                    # resultNum = spider.search_web(query="test", time=(datetime(2012, 1, 1), datetime(2012, 12, 31))).total
                    result = spider.search_web(query="test", time=(datetime(2012, 1, 1), datetime(2012, 12, 31)))
                    pprint(result.plain)

                    # resultList.append(f'{Id},{resultNum}\n')
                    curNum += 1
                    break
                except UnboundLocalError as e:
                    pprint(e)
                except Exception as e:
                    pprint(e)

                time.sleep(1)

            if curNum == 100:
                # write_result(f, resultList)
                curNum = 0
                resultList.clear()
        # write_result(f, resultList)


if __name__ == '__main__':
    init()

    df = pd.read_csv(src_filename)
    address_list = df['address']
    id_list = df['Id']

    n = 1
    total = len(df)
    batch = total // n + 1

    threads = []
    for i in range(0, n):
        start = i * batch
        end = (i + 1) * batch

        t = threading.Thread(target=thread_func, args=(id_list[start:end], address_list[start: end], i,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # 将临时文件合并
    # with open(target_filename, "w") as f:
    #     for i in range(0, n):
    #         with open(target_temp_filename_format.format(i), "r") as f1:
    #             f.write(f1.read())

    print("Exit Main Thread")


    #
    # resultList = []
    # spider = BaiduSpider()
    # f = open(target_filename, "w")
    #
    # i = 0
    # for Id, address in zip(id_list, address_list):
    #     resultNum = spider.search_web(query=address, time=(datetime(2012, 1, 1), datetime(2012, 12, 31))).total
    #
    #     result = "[{}] id:{} | address:{} | result:{}\n".format(
    #         time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), Id, address, resultNum)
    #     print(result, end='')
    #     resultList.append(f'{id},{resultNum}\n')

    #     i += 1
    #     if i == 1000:
    #         write_file(f, resultList)
    #         i = 0
    #         resultList.clear()  # 值为空
    # write_file(f, resultList)
    # f.close()

