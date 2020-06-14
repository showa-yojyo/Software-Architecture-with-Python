#!/usr/bin/env python
# Code Listing #5
"""

A simple web client using Twisted

"""

# twisted_fetch_url.py
import sys
# Twisted はイベント駆動型ネットワークエンジンをうたうフレームワーク。
# https://twistedmatrix.com/trac/
from twisted.internet import reactor
from twisted.web.client import getPage # DeprecationWarning...

# callback 1
def save_page(page, filename='content.html'):
    with open(filename, 'w') as f:
        f.write(page)
    print('Length of data', len(page))
    print(f'Data saved to {filename}')

# callback 2
def handle_error(error):
    print(error)


def finish_processing(value):
    print("Shutting down...")
    reactor.stop()


if __name__ == "__main__":
    url = sys.argv[1]
    deferred = getPage(url.encode('utf-8'))
    deferred.addCallbacks(save_page, handle_error)
    deferred.addBoth(finish_processing)

    reactor.run()
