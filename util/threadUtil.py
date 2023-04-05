import threading


class ThreadUtil:
    def __init__(self, n: int, func, args: list,):
        self.n = n
        self.func = func
        self.args = args

    def setFunc(self, func):
        self.func = func

    def run(self):
        total = len(self.args[0])
        batch = total // self.n + 1

        threads = []
        for i in range(0, self.n):
            start = i * batch
            end = (i + 1) * batch

            # todo:解耦
            t = threading.Thread(target=self.func, args=[self.args[0][start:end], self.args[1][start:end], i])
            t.start()
            print(f"Create thread-{i}, thread id: {t.ident}")
            threads.append(t)

        for t in threads:
            t.join()



