# Code Listing #6

"""

Find sub-strings in sequence1 using strings in sequence2.
Version with pympler memory usage detection.

"""

import random
import string
from pympler import asizeof

seq1, seq2 = [], []


def random_strings(n, N):

    global seq1, seq2
    for i in range(N):
        seq1.append(''.join(random.sample(string.ascii_lowercase,
                                          random.randrange(4, n))))

    for i in range(N):
        seq2.append(''.join(random.sample(string.ascii_lowercase,
                                          random.randrange(2, n/2))))


def slices(s, n):
    """Return all substrings in a string `s` with their length `n`.

    >>> slices('famicon', 3)
    ['fam', 'ami', 'mic', 'ico', 'con']
    """
    return [''.join(j) for j in zip(*(s[i:] for i in range(n)))]

# Uncomment for profiling with line or memory profiler
#@profile
def sub_string(seq1, seq2):
    """ Return sub-strings from seq2 which are part of strings in seq1
    - Optimized version
    """

    # E.g: seq1 = ['introduction','discipline','animation']
    # seq2 = ['in','on','is','mat','ton']
    # Result = ['in','on','mat','is']

    # Create all slices of lengths in a given range
    min_l, max_l = min(list(map(len, seq2))), max(list(map(len, seq2)))
    sequences = {}

    for i in range(min_l, max_l+1):
        for j in seq1:
            sequences.update({}.fromkeys(slices(j, i)))

    subs = []
    for item in seq2:
        if item in sequences:
            subs.append(item)
    print('Memory usage', asizeof.asized(sequences).format())

    return subs


def sub_string_brute(seq1, seq2):
    """ Sub-string by brute force """

    subs = []
    for item in seq2:
        for parent in seq1:
            if item in parent:
                subs.append(item)

    return subs


def test(N):
    random_strings(10, N)
    return sub_string(seq1, seq2)


def test2():
    return sub_string(seq1, seq2)


if __name__ == "__main__":
    from pympler import summary
    from pympler import muppy

    test(10000)
    all_objects = muppy.get_objects()
    sum1 = summary.summarize(all_objects)
    # 全オブジェクトの消費メモリを降順にリストする
    summary.print_(sum1)
