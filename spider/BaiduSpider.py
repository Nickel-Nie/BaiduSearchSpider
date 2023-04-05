import time


class BaiduSpider(object):
    def __init__(self, url, startYear: int, endYear: int):
        self.url = url

        # 处理限定时间的问题
        self.startYear = startYear  #限定年份
        self.endYear = endYear  #限定年份
        self.startTimestamp = 0
        self.endTimestamp = 0
        self.startTime = ""
        self.endTime = ""
        self.startTimeFormat = "{}-01-01 00:00:00"
        self.endTimeFormat = "{}-12-31 23:59:59"
        self.setTime(startYear, endYear)

    def setTime(self, startYear, endYear):
        def timeStringToTimestamp(string):
            timeArray = time.strptime(string, "%Y-%m-%d %H:%M:%S")
            timeStamp = int(time.mktime(timeArray))
            return timeStamp

        self.startTime = self.startTimeFormat.format(startYear)
        self.endTime = self.endTimeFormat.format(endYear)
        self.startTimestamp = timeStringToTimestamp(self.startTime)
        self.endTimestamp = timeStringToTimestamp(self.endTime)

    def run(self, Id, keyword)->int:
        pass
