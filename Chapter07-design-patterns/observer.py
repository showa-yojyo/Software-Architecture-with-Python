#!/usr/bin/env python
# Code Listing #14
"""

Example of publish subscribe

"""

import threading
import time

from datetime import datetime

# Publisher 役のクラス
class Alarm(threading.Thread):
    """ A class which generates periodic alarms """

    def __init__(self, duration=1):
        self.duration = duration
        # Subscribers
        self.subscribers = []
        self.flag = True
        super().__init__(None, None)

    def register(self, subscriber):
        """ Register a subscriber for alarm notifications """

        self.subscribers.append(subscriber)

    def notify(self):
        """ Notify all the subscribers """

        for subscriber in self.subscribers:
            subscriber.update(self.duration)

    def stop(self):
        """ Stop the thread """

        self.flag = False

    # Thread からのオーバーライドメソッドはこれしかない
    def run(self):
        """ Run the alarm generator """

        while self.flag:
            time.sleep(self.duration)
            # Notify
            self.notify()

# Subscriber 役のクラス
class DumbClock:
    """ A dumb clock class using an Alarm object """

    def __init__(self, name):
        # Start time
        self.current = time.time()
        self.name = name

    def update(self, *args):
        """ Callback method from publisher """

        self.current += args[0]
        print(self)

    def __str__(self):
        """ Display local time """

        return f'{self.name} {datetime.fromtimestamp(self.current):%H:%M:%S}'

def main():
    publisher = Alarm()
    publisher.register(DumbClock("1"))
    publisher.register(DumbClock("2"))
    publisher.register(DumbClock("3"))
    publisher.start()

    time.sleep(3)
    publisher.stop()

if __name__ == "__main__":
    main()
