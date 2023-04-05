import re
import time
import requests

from lxml import etree

from config import logger
from .BaiduSpider import BaiduSpider


class BaiduSpiderRequest(BaiduSpider):
    def __init__(self, url, startYear: int, endYear: int):
        BaiduSpider.__init__(self, url, startYear, endYear)

        self.cookies = {
            'BIDUPSID': 'A76367BB28D7ED1DEFF85DF37E31EEB5',
            'PSTM': '1561214638',
            'BAIDUID': 'E71A90307FC0D94471C70B3FF600E82C:SL=0:NR=10:FG=1',
            'BDUSS': 'MzZE5XQkZCaUVCbHJPWGFpcGNMUXIycS11RXkyN3Fxb3hRWDRVUUhubndjNnBnSVFBQUFBJCQAAAAAAAAAAAEAAAAUBZIUwLax-aHi0vS2-QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPDmgmDw5oJgOU',
            'BDUSS_BFESS': 'MzZE5XQkZCaUVCbHJPWGFpcGNMUXIycS11RXkyN3Fxb3hRWDRVUUhubndjNnBnSVFBQUFBJCQAAAAAAAAAAAEAAAAUBZIUwLax-aHi0vS2-QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPDmgmDw5oJgOU',
            'BD_UPN': '12314753',
            'BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
            'delPer': '0',
            'BD_CK_SAM': '1',
            'PSINO': '6',
            'BAIDUID_BFESS': 'E71A90307FC0D94471C70B3FF600E82C:SL=0:NR=10:FG=1',
            'COOKIE_SESSION': '143_0_3_3_1_3_0_0_3_2_2_0_0_0_8_0_1672146809_0_1672146801%7C3%230_0_1672146801%7C1',
            'BA_HECTOR': '2h21akak2ka4a1852k2ka57c1i1lui71m',
            'ZFY': '23HPinq563xo7:AQjYc:AqX4sL98:Avpsm0lbn:A:Ar23l5w:C',
            'BD_HOME': '1',
            'BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0',
            'H_PS_PSSID': '38185_36560_38368_37861_38170_38290_38221_38262_37924_38313_38382_38040_26350_22158_38283_37881',
            'H_PS_645EC': 'cd78PCtt9bsjnDDsLuKfLcIx%2Fl6otxBWLFHbz0CdJZ5zgRB0ywTbiSm6ZKAV69soEcyA',
            'BDSVRTM': '219',
        }

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=31536000',
            'Connection': 'keep-alive',
            'Referer': 'https://cn.bing.com/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Microsoft Edge";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.params = {
            'wd': '',
            'rsv_spt': '1',
            'rsv_iqid': '0x9e046da7000d2ab8',
            'issp': '1',
            'f': '8',
            'rsv_bp': '1',
            'rsv_idx': '2',
            'ie': 'utf-8',
            'tn': 'baiduhome_pg',
            'rsv_enter': '0',
            'rsv_dl': 'tb',
            'rsv_sug3': '3',
            'rsv_n': '2',
            'rsv_btype': 'i',
            'inputT': '1706',
            'rsv_sug4': '8863',
            'gpc': f'stf={self.startTimestamp},{self.endTimestamp}|stftype=2'  # 搜索时间
        }

    def run(self, Id, keyword)->int:
        self.params['wd'] = keyword  # 填充关键词

        while True:
            response = requests.get(self.url, headers=self.headers, params=self.params,
                                    cookies=self.cookies)
            connect = etree.HTML(response.content)
            g_list = connect.xpath('//*[@id="tsn_inner"]/div[2]/span/text()')
            if len(g_list) > 0:
                g = g_list[0]
                g = ''.join(g)
                g_num_list = re.findall('[0-9]\d*', g)
                if len(g_num_list) > 0:
                    g = g_num_list[0]
                    # print(g)
                    return g
                else:
                    g = ""
                    logger.error(f"id:{Id}, detail:无法匹配到数字")
                    # print("无法匹配到数字")
            else:
                g = ""
                logger.error(f"id:{Id}, detail:未匹配到需要的元素")
                # print("未匹配到需要的元素")

            time.sleep(1)  # 每次循环暂停1秒，避免频繁请求服务器被封IP

