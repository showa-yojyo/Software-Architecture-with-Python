# Code listing #18

""" Module urlrank - Rank URLs in order of degree of a specific word frequency """

import operator
import requests


class UrlRank:
    """ Accept URLs as inputs and rank them in
    terms of how much a word occurs in them """

    def __init__(self, word, *urls):
        self.word = word.strip().lower()
        self.urls = urls

    def rank(self):
        """ Rank the URLs. A tuple is returned with
        (url, #occur) in decreasing order of
        occurences """

        occurs = []

        for url in self.urls:
            # この次の行しか textrank.py との違いはなかった。
            data = requests.get(url).content
            words = [x.lower().strip() for x in data.split()]
            # Filter empty words
            count = words.count(self.word)
            occurs.append((url, count))

        # Return in sorted order
        return sorted(occurs, key=operator.itemgetter(1), reverse=True)
