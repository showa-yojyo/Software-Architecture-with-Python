# Code listing #20

""" Module textrank - Rank text files in order of degree of a specific word frequency. """

# Note: This is textrank.py rewritten to use rankbase, so called textrank2.py

from rankbase import RankBase


class TextRank(RankBase):
    """ Accept text files as inputs and rank them in
    terms of how much a word occurs in them """

    def __init__(self, word, *filenames):
        super().__init__(word)
        self.filenames = filenames

    # XXX: オーバーライドのようでそうでない。
    def rank(self):
        """ Rank the files. A tuple is returned with
        (filename, #occur) in decreasing order of
        occurences """

        texts = []
        for filename in self.filenames:
            with open(filename, encoding='utf-8') as fp:
                texts.extend(fp.read())
        occurs = super().rank(*texts)
        # Convert to filename list
        occurs = [(self.filenames[x], y) for x, y in occurs.items()]

        return self.sort(occurs)


if __name__ == "__main__":
    import sys
    print(TextRank('common', *sys.argv[1:]).rank())
