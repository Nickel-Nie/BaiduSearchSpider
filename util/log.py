import logging
import os
import queue
import threading
from logging import handlers

# log_filename = './log/baiduSpider.log'

# s = sched.scheduler(time.time, time.sleep)


class LogFactory:
    def __init__(self, name):
        debug_filename = name + "_info.log"
        error_filename = name + "_error.log"
        formatter = logging.Formatter("[%(asctime)s] - %(levelname)s - %(message)s")

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)  # 设置日志记录器级别为 DEBUG

        # add the handlers to the logger

        self.logger.addHandler(LogFactory.createHandler(debug_filename, logging.INFO, formatter))
        info_filter = logging.Filter()

        self.logger.addHandler(LogFactory.createHandler(error_filename, logging.ERROR, formatter))

    @classmethod
    def createHandler(cls, filename, level, formatter):
        handler = logging.FileHandler(filename, encoding='utf-8')
        handler.setLevel(level)
        handler.setFormatter(formatter)
        # handler.propagate = False

        level_filter = logging.Filter()
        level_filter.filter = lambda record: record.levelno == level  # 设置过滤等级
        handler.addFilter(level_filter)

        return handler

    def getLogger(self):
        return self.logger


class MyLog(threading.Thread):
    def __init__(self, fileName):
        threading.Thread.__init__(self)
        self.name = fileName
        self.m_dataQueue = queue.Queue()
        self.m_running = False

        filePath = os.path.join(os.path.abspath('.'), 'log')
        if not os.path.exists(filePath):
            os.mkdir(filePath)

        fileName = os.path.join(filePath, fileName)
        self.logger = LogFactory(fileName).getLogger()

    def run(self):
        self.m_running = True
        while self.m_running:
            data = self.m_dataQueue.get()
            if data is None:
                continue

            loglevel = list(data.keys())[0]
            content = list(data.values())[0]
            # 暂时只用到info 和 error两个级别
            if 'debug' == loglevel:
                self.logger.debug(*content)
            elif 'info' == loglevel:
                self.logger.info(*content)
            elif 'warning' == loglevel:
                self.logger.warning(*content)
            elif 'error' == loglevel:
                self.logger.error(*content)
            elif 'critical' == loglevel:
                self.logger.critical(*content)

    def stop(self):
        self.m_running = False
        self.m_dataQueue.put(None)

    # def debug(self, *content):
    #     self.m_dataQueue.put({'debug': content})

    def info(self, *content):
        self.m_dataQueue.put({'info': content})

    # def warning(self, *content):
    #     self.m_dataQueue.put({'warning': content})

    def error(self, *content):
        self.m_dataQueue.put({'error': content})

    # def critical(self, *content):
    #     self.m_dataQueue.put({'critical': content})


# logDebug = MyLog('bar_debug.log')
# logDebug.setDaemon(True)
# logDebug.start()
#
# logInfo = MyLog('bar_info.log')
# logInfo.setDaemon(True)
# logInfo.start()
#
# logError = MyLog('bar_error.log')
# logError.setDaemon(True)
# logError.start()
#
# logHqRecv = MyLog('bar_hq.log')
# logHqRecv.setDaemon(True)
# logHqRecv.start()
#
# logCritical = MyLog('bar_critical.log')
# logCritical.setDaemon(True)
# logCritical.start()
#
# logHeartBeat = MyLog('bar_heartbeat.log')
# logHeartBeat.setDaemon(True)
# logHeartBeat.start()
#
# logNotInTradeTime = MyLog('bar_notintradetime.log')
# logNotInTradeTime.setDaemon(True)
# logNotInTradeTime.start()
#
# logSql = MyLog('bar_sql.log')
# logSql.setDaemon(True)
# logSql.start()
