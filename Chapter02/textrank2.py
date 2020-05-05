# Code listing #20

""" Module textrank - Rank text files in order of degree of a specific word frequency. """

# Note: This is textrank.py rewritten to use rankbase, so called textrank2.py

import operator
from rankbase import RankBase


class TextRank:
    """ Accept text files as inputs and rank them in
    terms of how much a word occurs in them """

    def __init__(self, word, *filenames):
        self.word = word.strip().lower()
        self.filenames = filenames

    def rank(self):
        """ Rank the files. A tuple is returned with
        (filename, #occur) in decreasing order of
        occurences """

        occurs = []

        for fpath in self.filenames:
            with open(fpath) as f:
                data = f.read()
            words = [x.lower().strip() for x in data.split()]
            # Filter empty words
            count = words.count(self.word)
            occurs.append((fpath, count))

        # Return in sorted order
        return sorted(occurs, key=operator.itemgetter(1), reverse=True)


class TextRank(RankBase):
    """ Accept text files as inputs and rank them in
    terms of how much a word occurs in them """

    def __init__(self, word, *filenames):
        self.word = word.strip().lower()
        self.filenames = filenames

    def rank(self):
        """ Rank the files. A tuple is returned with
        (filename, #occur) in decreasing order of
        occurences """

        texts = []
        for filename in self.filenames:
            with open(filename) as fp:
                texts.extend(fp.read())
        occurs = super().rank(*texts)
        # Convert to filename list
        occurs = [(self.filenames[x], y) for x, y in occurs.items()]

        return self.sort(occurs)


if __name__ == "__main__":
    import sys
    print(TextRank('common', *sys.argv[1:]).rank())
