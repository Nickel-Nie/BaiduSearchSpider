import re

import requests
from lxml import etree
import pandas as pd
import time

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    "Accept-Encoding": "gzip, deflate, br",
    'Host': 'www.baidu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Cookie': 'BIDUPSID=9171763CFDBF80384A3DCBEA380B8C1E; PSTM=1648111648; BDUSS=lGakpDSlROcnZoVkY3aDhvbVB1SDczR29lcFVJcnpSSmNRTVlYVlNrak1vLXhmRVFBQUFBJCQAAAAAAAAAAAEAAADgj2NFc2gxdNi8OTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMwWxV%7EMFsVfdz; BDUSS_BFESS=lGakpDSlROcnZoVkY3aDhvbVB1SDczR29lcFVJcnpSSmNRTVlYVlNrak1vLXhmRVFBQUFBJCQAAAAAAAAAAAEAAADgj2NFc2gxdNi8OTcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMwWxV%7EMFsVfdz; BD_UPN=123253; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID=441A2B6CE04AA2666BE28E16650BAB96:FG=1; sugstore=0; H_PS_PSSID=38185_36545_38410_38470_38368_38305_38468_38289_37920_38383_26350_38421_38283_37881; BAIDUID_BFESS=441A2B6CE04AA2666BE28E16650BAB96:FG=1; delPer=0; BD_CK_SAM=1; PSINO=1; H_PS_645EC=daed6GQC7sE%2BVugjVLtQqIpVQ%2BD0SZU5GUPlwwHg1svwfHYWc%2FBMTNQKjwQvVvOMeEGj; BA_HECTOR=al2084a48k8g21a52085241f1i29skm1n; BDSVRTM=315; ZFY=ZsBnLhwkEgUGCRjjsjwQFdx:ADtePGMRr:ARASm4l5dUQ:C; baikeVisitId=6edea896-91bc-407a-8b58-880ac1d5b5eb'
}

# params = (
#     ('wd', f'{wd}'),
#     ('rsv_spt', '1'),
#     ('rsv_iqid', '0x9e046da7000d2ab8'),
#     ('issp', '1'),
#     ('f', '8'),
#     ('rsv_bp', '1'),
#     ('rsv_idx', '2'),
#     ('ie', 'utf-8'),
#     ('tn', 'baiduhome_pg'),
#     ('rsv_enter', '0'),
#     ('rsv_dl', 'tb'),
#     ('rsv_sug3', '3'),
#     ('rsv_n', '2'),
#     ('rsv_btype', 'i'),
#     ('inputT', '1706'),
#     ('rsv_sug4', '8863'),
#     ('gpc', 'stf=1325347200,1356969599|stftype=2')  # 搜索时间
# )

params = {
    "gpc" : "stf=1325347200,1356969599|stftype=2",
    'ie': 'utf-8',
    'wd': '',  #待更换
}

def get_connect(Id, wd):
    params['wd'] = wd

    # response = requests.get('https://www.baidu.com/s', headers=headers, params=params, cookies=cookies)

    while True:
        response = requests.get('https://www.baidu.com/s', headers=headers, params=params)
        connect = etree.HTML(response.content)
        g_list = connect.xpath('//*[@id="tsn_inner"]/div[2]/span/text()')
        if len(g_list) > 0:
            g = g_list[0]
            g = ''.join(g)
            g_num_list = re.findall('[0-9]\d*', g)
            if len(g_num_list) > 0:
                g = g_num_list[0]
                print(g)
                with open('baidu.csv', 'a+') as f:
                    f.write(f'{Id},{g}\n')
                break  # 获取数据后跳出循环
            else:
                g = ""
                print("无法匹配到数字")
        else:
            g = ""
            print("未匹配到需要的元素")
        time.sleep(1)  # 每次循环暂停1秒，避免频繁请求服务器被封IP


if __name__ == '__main__':
    df = pd.read_csv(r'occurrenceFile/_2012_occurrence.csv')
    address_list = df['address']
    id_list = df['Id']
    for Id, address in zip(id_list, address_list):
        get_connect(Id, address)
