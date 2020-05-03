# Code listing #17

""" Module textrank - Rank text files in order of degree of a specific word frequency. """

import operator


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
        # このコードの急所はここの key=operator.itemgetter(1)
        return sorted(occurs, key=operator.itemgetter(1), reverse=True)
