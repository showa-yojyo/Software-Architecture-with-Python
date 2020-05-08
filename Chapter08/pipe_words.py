#!/usr/bin/env python
# Code Listing #10
"""

Simple example of pipe and filter - A program counting words in a file

"""


# pipe_words.py
from multiprocessing import Process, Pipe
import sys

# process 1
def read(filename, conn):
    """ Read data from a file and send it to a pipe """

    with open(filename, encoding='utf-8') as f:
        conn.send(f.read())

# process 2
def words(conn):
    """ Read data from a connection and print number of words """

    data = conn.recv()
    print('Words', len(data.split()))


if __name__ == "__main__":
    # Pipe() および Process() の使い方
    parent, child = Pipe() # 返り値の拾い方が独特
    p1 = Process(target=read, args=(sys.argv[1], child))
    p1.start()
    p2 = Process(target=words, args=(parent,))
    p2.start()
    p1.join()
    p2.join()
