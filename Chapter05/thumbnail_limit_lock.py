# Code Listing #3

"""

Thumbnail producer/consumer - Limiting number of images using a lock

"""

import threading
import time
import string
import random
import uuid
import urllib.request
from PIL import Image
from queue import Queue

# このクラスは変更なし
class ThumbnailURL_Generator(threading.Thread):
    """ Worker class that generates image URLs """

    def __init__(self, queue, sleep_time=1,):
        self.sleep_time = sleep_time
        self.queue = queue
        # A flag for stopping
        self.flag = True
        # sizes
        self._sizes = (240, 320, 360, 480, 600, 720)
        # URL scheme
        self.url_template = 'https://dummyimage.com/%s/%s/%s.jpg'
        super().__init__()

    def __str__(self):
        return 'Producer'

    def get_size(self):
        return '%dx%d' % (random.choice(self._sizes),
                          random.choice(self._sizes))

    def get_color(self):
        return ''.join(random.sample(string.hexdigits[:-6], 3))

    def run(self):
        """ Main thread function """

        while self.flag:
            # generate image URLs of random sizes and fg/bg colors
            url = self.url_template % (self.get_size(),
                                       self.get_color(),
                                       self.get_color())
            # Add to queue
            print(self, 'Put', url)
            self.queue.put(url)
            time.sleep(self.sleep_time)

    def stop(self):
        """ Stop the thread """

        self.flag = False

# Lock を利用するクラス
# 例えば 500 個を上限としているときにファイル保存の回数が 500 を超えないように
# するにはロックの仕組みなどを用いるのが自然だ。
class ThumbnailImageSaver:
    """ Class which saves URLs to thumbnail images and keeps a counter """

    def __init__(self, limit=10):
        self.limit = limit
        self.lock = threading.Lock()
        self.counter = {}

    def thumbnail_image(self, url, size=(64, 64), format='.png'):
        """ Save image thumbnails, given a URL """

        im = Image.open(urllib.request.urlopen(url))
        # filename is last two parts of URL minus extension + '.format'
        pieces = url.split('/')
        filename = ''.join(
            (pieces[-2], '_', pieces[-1].split('.')[0], '_thumb', format))
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(filename)
        print('Saved', filename)
        self.counter[filename] = 1 # 一見妙だが？
        return True

    # ディスクへの保存をロックする
    def save(self, url):
        """ Save a URL as thumbnail """

        with self.lock:
            # ロックしてから変数を参照するのが急所
            if len(self.counter) >= self.limit:
                return False
            self.thumbnail_image(url)
            print('\tCount=>', len(self.counter))
            return True


class ThumbnailURL_Consumer(threading.Thread):
    """ Worker class that consumes URLs and generates thumbnails """

    def __init__(self, queue, saver):
        self.queue = queue
        self.flag = True
        # Saver を組み込む
        self.saver = saver
        self.count = 0
        # Internal id
        # uuid.uuid4() の応用例
        self._id = uuid.uuid4().hex
        super().__init__(name='Consumer-' + self._id)

    def __str__(self):
        return 'Consumer-' + self._id

    def run(self):
        """ Main thread function """

        while self.flag:
            url = self.queue.get()
            print(self, 'Got', url)
            self.count += 1
            # Saver の保存メソッドに差し替える
            if not self.saver.save(url):
                # Limit reached, break out
                print(self, 'Set limit reached, quitting')
                break # 今度は自分から止まる

    def stop(self):
        """ Stop the thread """

        self.flag = False


if __name__ == '__main__':
    from queue import Queue
    import glob
    #import os

    # コメントアウトしておく
    #os.system('rm -f *.png')
    q = Queue(maxsize=2000)
    saver = ThumbnailImageSaver(limit=50)

    producers, consumers = [], []
    for i in range(3):
        t = ThumbnailURL_Generator(q)
        producers.append(t)
        t.start()

    # Saver を Consumer 全部に渡す
    for i in range(5):
        t = ThumbnailURL_Consumer(q, saver)
        consumers.append(t)
        t.start()

    # Consumer 側を全部 join() する
    # スレッドが終了するまで待機（ブロック）する。
    for t in consumers:
        t.join()
        print('Joined', t, flush=True)

    # To make sure producers dont block on a full queue
    # キューを手動で空にする？
    while not q.empty():
        item = q.get()

    # それから Generator 側すべてに対してフラグをリセットする
    for t in producers:
        t.stop()
        print('Stopped', t, flush=True)

    # サムネイルの個数をファイルシステムから得る
    print('Total number of PNG images', len(glob.glob('*.png')))
