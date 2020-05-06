#!/usr/bin/env python
# Code Listing - #3

"""

StreamHasher - Class providing hashing of data from an input stream
using pluggable algorithms

"""

# NOTE: This combines the two methods provided in the book into one class.


class StreamHasher:
    """ Stream hasher class with configurable algorithm """

    # callable を受け取る
    def __init__(self, algorithm, chunk_size=4096):
        self.chunk_size = chunk_size
        self.hash = algorithm()

    def get_hash(self, stream):
        """ Return the hash digest """

        for chunk in iter(lambda: stream.read(self.chunk_size), ''):
            self.hash.update(chunk.encode('utf-8'))

        return self.hash.hexdigest()

    def __call__(self, stream):

        return self.get_hash(stream)


if __name__ == "__main__":
    from hashlib import md5, sha1

    # Both works
    with open('hasher.py', encoding='utf-8') as f:
        md5h = StreamHasher(algorithm=md5)
        print(md5h(f))

    with open('hasher.py', encoding='utf-8') as f:
        shah_h = StreamHasher(algorithm=sha1)
        print(shah_h(f))
