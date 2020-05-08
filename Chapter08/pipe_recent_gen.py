#!/usr/bin/env python
# Code Listing #12
"""

Using generators, print details of the most recently modified file, matching a pattern.

"""

# pipe_recent_gen.py

import glob
import os
import subprocess
from time import sleep


def watch(pattern):
    """ Watch a folder for modified files matching a pattern """

    while True:
        # sort by modified time
        # stat ベースの最終更新
        files = sorted(glob.glob(pattern), key=os.path.getmtime)
        if files:
            recent = files[-1]
            yield recent
        # Sleep a bit
        sleep(1)


def get(input):
    """ For a given file input, print its meta data """

    for item in input:
        # popen() はパイプ I/O
        # この方式は UnicodeDecodeError が送出されて苦しい
        #data = os.popen(f"ls -lh {item}").read()
        data = subprocess.check_output(['ls', '-lh', f'{item}']).decode('utf-8')

        # Clear screen
        os.system("clear")
        yield data


if __name__ == "__main__":
    import sys

    # Source
    stream1 = watch('*.' + sys.argv[1])

    while True:
        # Filter
        stream2 = get(stream1)
        print(next(stream2))
        sleep(2)
