# Code Listing #4

"""

Thumbnail producer/consumer - Limiting number of images using a Semaphore.

"""

import threading
import time
import string
import random
import uuid
import urllib.request

from PIL import Image
from queue import Queue

# Generator は無限生成版、ロック版と同じ定義
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

# Saver は Lock を Semaphore に変更する
class ThumbnailImageSemaSaver:
    """ Class which keeps an exact counter of saved images
    and restricts the total count using a semaphore """

    def __init__(self, limit=10):
        self.limit = limit
        # BoundedSemaphore は初見だ
        self.counter = threading.BoundedSemaphore(value=limit)
        self.count = 0
        # Start time
        self.start = time.time()
        # Image saving rate
        self.rate = 0

    def acquire(self):
        # Acquire counter, if limit is exhausted, it
        # returns False
        return self.counter.acquire(blocking=False)

    def release(self):
        # Release counter, incrementing count
        return self.counter.release()

    def thumbnail_image(self, url, size=(64, 64), format='.png'):
        """ Save image thumbnails, given a URL """

        im = Image.open(urllib.request.urlopen(url))
        # filename is last two parts of URL minus extension + '.format'
        pieces = url.split('/')
        filename = ''.join((pieces[-2], '_', pieces[-1].split('.')[0], format))

        # 急所の例外処理
        try:
            im.thumbnail(size, Image.ANTIALIAS)
            im.save(filename)
            print('Saved', filename)
            self.count += 1
        except Exception as e:
            print('Error saving URL', url, e)
            # Image can't be counted, increment semaphore
            self.release()

        return True

    def save(self, url):
        """ Save a URL as thumbnail """

        # セマフォの許しが出てから保存を呼び出すものとする
        # 残念なことに with 文のほうがみてくれが良かった
        if self.acquire(): # blocking=False
            self.thumbnail_image(url)
            return True
        else:
            print('Semaphore limit reached, returning False')
            return False

# Consumer は変更なし
class ThumbnailURL_Consumer(threading.Thread):
    """ Worker class that consumes URLs and generates thumbnails """

    def __init__(self, queue, saver):
        self.queue = queue
        self.flag = True
        self.saver = saver
        self.count = 0
        # Internal id
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
            if not self.saver.save(url):
                # Limit reached, break out
                print(self, 'Set limit reached, quitting')
                break

    def stop(self):
        """ Stop the thread """

        self.flag = False

# メイン処理は変更なし
if __name__ == '__main__':
    from queue import Queue
    import glob
    #import os

    #os.system('rm -f *.png')
    q = Queue(maxsize=2000)
    saver = ThumbnailImageSemaSaver(limit=100)

    producers, consumers = [], []
    for i in range(3):
        t = ThumbnailURL_Generator(q)
        producers.append(t)
        t.start()

    for i in range(5):
        t = ThumbnailURL_Consumer(q, saver)
        consumers.append(t)
        t.start()

    for t in consumers:
        t.join()
        print('Joined', t, flush=True)

    # To make sure producers dont block on a full queue
    while not q.empty():
        _ = q.get()

    for t in producers:
        t.stop()
        print('Stopped', t, flush=True)

    print('Total number of PNG images', len(glob.glob('*.png')))
