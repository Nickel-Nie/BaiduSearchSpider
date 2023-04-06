import threading


class ThreadUtil:
    def __init__(self, n: int, func, *args):
        self.n = n
        self.func = func
        self.args = args

    def setFunc(self, func):
        self.func = func

    def run(self):
        threads = []
        for i in range(0, self.n):
            # 解耦,每个线程所获取的切片在类外部完成
            t = threading.Thread(target=self.func, args=[self.args[0][i], self.args[1][i], i])
            t.start()
            print(f"Create thread-{i}, thread id: {t.ident}")
            threads.append(t)

        for t in threads:
            t.join()



