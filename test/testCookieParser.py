from util.cookieParser import cookie_parser, param_parser

cookieFile = r"Z:\UESTC\Code\Python\BaiduSpider\util\cookies.txt"
paramFile = r"Z:\UESTC\Code\Python\BaiduSpider\util\params.txt"

# cookies = cookie_parser(cookieFile)
# for key,value in cookies.items():
#     print(f"{key} = {value}")

params = param_parser(paramFile)
for key,value in params.items():
    print(f"{key} = {value}")