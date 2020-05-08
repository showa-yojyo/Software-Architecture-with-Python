#!/usr/bin/env python
# Code Listing #11
"""

A simple data processing pipeline using generators to print count of words in files.

"""

# pipe_words_gen.py
import os # listdir() を使う


def read(filenames):
    """ Generator that yields data from filenames as (filename, data) tuple """

    for filename in filenames:
        with open(filename, encoding='utf-8') as f:
            yield filename, f.read()


def words(input):
    """ Generator that calculates words in its input """

    for filename, data in input:
        yield filename, len(data.split())

# これと同じことをするものが標準にある。
def filter(input, pattern):
    """ Filter input stream according to a pattern """

    for item in input:
        if item.endswith(pattern):
            yield item


if __name__ == "__main__":
    # Source
    stream1 = filter(os.listdir('.'), '.py')
    # Piped to next filter
    stream2 = read(stream1)
    # Piped to last filter (sink)
    stream3 = words(stream2)

    # すなわち words(read(filter(os.listdir('.'), '.py')))

    for item in stream3:
        print(item)
