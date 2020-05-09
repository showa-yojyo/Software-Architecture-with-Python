# Code listing #21

""" Module urlrank - Rank URLs in order of degree of a specific word frequency """

# Note: This is urlrank.py rewritten to use rankbase so called urlrank2.py

import operator
import requests
from rankbase import RankBase


class UrlRank(RankBase):
    """ Accept URLs as inputs and rank them in
    terms of how much a word occurs in them """

    def __init__(self, word, *urls):
        super().__init__(word)
        self.urls = urls

    # これもオーバーライドではなくなっている
    def rank(self):
        """ Rank the URLs. A tuple is returned with
        (url, #occur) in decreasing order of
        occurences """

        texts = [requests.get(x).content for x in self.urls]
        occurs = super().rank(*texts)
        # Convert to URLs list
        occurs = [(self.urls[x], y) for x, y in occurs.items()]

        return self.sort(occurs)


if __name__ == "__main__":
    import sys
    print(UrlRank('python', *sys.argv[1:]).rank())
