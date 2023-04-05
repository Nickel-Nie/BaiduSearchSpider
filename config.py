from datetime import datetime
from util import log
from util.log import MyLog

year = 2014
version = "request"  # 只有selenium和request两种版本。

# 文件名称相关
src_filename = f"./occurrenceFile/{year}_occurrence.csv"
target_filename = f"./result/{version}/{year}_baidu_result.csv"
target_temp_filename_format = "./temp/" + version + "/" + str(year) + "_baidu_result_temp_{}.csv"

# 日志相关
log_filename = f"{year}_baidu_result_{datetime.now().strftime('%Y_%m_%d')}"  # 这里不加.log
# logger = log.LogFactory(log_filename).getLogger()
# 设置守护进程
logger = MyLog(log_filename)
logger.setDaemon(True)
