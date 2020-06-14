# Code Listing #6

"""

Primality checker - using multiple threads

Run this as,

$ time python3 prime_thread.py > /dev/null

"""

import threading
from queue import Queue, Empty

# 数学的な処理は変更なし
def is_prime(n):
    """ Check for input number primality """

    for i in range(3, int(n**0.5+1), 2):
        if n % i == 0:
            print(n, 'is not prime')
            return False

    print(n, 'is prime')
    return True


class PrimeChecker(threading.Thread):
    """ Thread class for primality checking """

    def __init__(self, queue):
        self.queue = queue # 共有キュー
        self.flag = True # 内部フラグ
        super().__init__()

    def run(self):
        # 内部フラグがリセットされるまでループ
        while self.flag:
            try:
                # get() のタイムアウトとは？
                is_prime(self.queue.get(timeout=1))
            except Empty: # こんな例外名なのか
                break

    # 呼び出されないメソッド
    def stop(self):
        """ Stop the thread """

        self.flag = False


if __name__ == "__main__":
    numbers = [1297337, 1116281, 104395303,
               472882027, 533000389, 817504243,
               982451653, 112272535095293,
               115280095190773, 1099726899285419]*100
    q = Queue(1000)

    # スレッド開始前にテストする数をキューに格納する
    for n in numbers:
        q.put(n)

    # 4 スレッドを開始する
    threads = []
    for i in range(4):
        t = PrimeChecker(q)
        threads.append(t)
        t.start()

    # 終了するまで待機する
    for t in threads:
        t.join()
