# Code Listing #9
# これは意味がわからない。
"""

Sort a number of disk files using a counter - a dictionary that keeps counts of numbers.

"""

# sort_counter.py
import sys
import collections

MAXINT = 100000


def sort():
    """ Sort files on disk by using a counter """

    counter = collections.defaultdict(int)

    for i in range(int(sys.argv[1])):
        filename = 'numbers/numbers_%d.txt' % i
        with open(filename) as f:
            for n in f:
                counter[n] += 1

    print('Sorting...')

    with open('sorted_nums.txt', 'w') as fp:
        # バケツソート的な着想
        for i in range(1, MAXINT+1):
            # '\n' が要るのがダサい
            text = str(i) + '\n'
            # 単純に counter[text] でも動作するだろう
            if (count := counter.get(text, 0)) > 0:
                fp.write(text * count)

    print('Sorted')


if __name__ == "__main__":
    sort()
