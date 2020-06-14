#!/usr/bin/env python
# Code Listing #2
"""

Thumbnail converter using producer-consumer architecture

"""

from queue import Queue
import threading
import time
import string
import random
import urllib.request

from PIL import Image

# Thread のサブクラスを二つ定義する。Generator と Consumer だ。


class ThumbnailURL_Generator(threading.Thread):
    """ Worker class that generates image URLs """

    def __init__(self, queue, sleep_time=1,):
        self.sleep_time = sleep_time

        # Generator はキューを受け取り、ここに処理するべきものを押し込んでいく。
        self.queue = queue
        # A flag for stopping
        self.flag = True
        # sizes
        self._sizes = (240, 320, 360, 480, 600, 720)
        # URL scheme
        self.url_template = 'https://dummyimage.com/%s/%s/%s.jpg' # これはクラス変数でよい
        super().__init__()

    def __str__(self):
        return 'Producer'

    # 返り値が毎回異なると思ってよい
    def get_size(self):
        return '%dx%d' % (random.choice(self._sizes),
                          random.choice(self._sizes))

    # 返り値が毎回異なると思ってよい
    def get_color(self):
        # string.hexdigits の利用法として面白い
        return ''.join(random.sample(string.hexdigits[:-6], 3))

    def run(self):
        """ Main thread function """

        while self.flag: # このスレッドが生きている間は
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


class ThumbnailURL_Consumer(threading.Thread):
    """ Worker class that consumes URLs and generates thumbnails """

    def __init__(self, queue):
        # Consumer 側もキューを受け取る
        self.queue = queue
        self.flag = True
        super().__init__(name='Consumer')

    def __str__(self):
        return 'Consumer'

    # PIL を用いてサムネイル画像をディスクに保存する
    def thumb_image(self, url, size=(64, 64), format='.png'):
        """ Save image thumbnails, given a URL """

        im = Image.open(urllib.request.urlopen(url))
        # filename is last part of URL minus extension + '.format'
        filename = url.split('/')[-1].split('.')[0] + '_thumb' + format
        im.thumbnail(size, Image.ANTIALIAS)
        im.save(filename)
        print(self, 'Saved', filename)

    def run(self):
        """ Main thread function """

        while self.flag: # スレッドが生きている間は
            # Consumer 側ではキューから処理するべきものを引き抜く
            url = self.queue.get()
            print(self, 'Got', url)
            self.thumb_image(url)

    def stop(self):
        """ Stop the thread """

        self.flag = False
        self.join() # Consumer 側の中止処理で join() する


if __name__ == '__main__':
    import glob

    # キューは Generator, Consumer の外で持つ
    q = Queue(maxsize=200)

    # Generator も Consumer も複数のオブジェクトがあり得る
    producers, consumers = [], []

    # Generetor を 2 個生成してスレッドを開始する
    for i in range(2):
        t = ThumbnailURL_Generator(q)
        producers.append(t)
        t.start()

    # その後に Consumer を 2 個生成してスレッドを開始する
    for i in range(2):
        t = ThumbnailURL_Consumer(q)
        consumers.append(t)
        t.start()

    # 以下は追加コード

    time.sleep(5)

    # Consumer スレッドをブロックしながら停止する
    for t in consumers:
        t.stop()

    # To make sure producers dont block on a full queue
    while not q.empty():
        _ = q.get()

    # Producer スレッドをノンブロッキングで停止する
    for t in producers:
        t.stop()
        print('Stopped', t, flush=True)

    print('Total number of PNG images', len(glob.glob('*.png')))
