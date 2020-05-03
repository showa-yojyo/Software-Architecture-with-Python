# Code listing #14

""" Module B (b.py) - Provides text processing functions to user """

# Note: This is the text processing version of b so called b_text.py

import a_text as a


def common(string1, string2):
    """ Return common words across strings1 1 & 2 """

    s1 = set(string1.lower().split())
    s2 = set(string2.lower().split())
    return s1.intersection(s2)


def common_words(filename1, filename2):
    """ Return common words across two input files """

    with open(filename1) as file1, open(filename2) as file2:
        lines1 = file1.read()
        lines2 = file2.read()

    return a.common_words(lines1, lines2)
