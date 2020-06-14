# Code Listing #10
# これは意味がわからない。

"""

Sort a number of disk files using a counter using multiple processes

"""

# sort_counter_mp.py
import sys
import time
import collections
from multiprocessing import Pool

MAXINT = 100000

# これは前回のバケツソートと同じ
def sorter(filenames):
    """ Sorter process sorting files using a counter """

    counter = collections.defaultdict(int)

    for filename in filenames:
        with open(filename) as f:
            # やはり文字列をキーとする
            for i in f:
                counter[i] += 1

    return counter


def batch_files(pool_size, limit):
    """ Create batches of files to process by a multiprocessing Pool """

    batch_size = limit // pool_size

    filenames = []

    for i in range(pool_size):
        batch = ['numbers/numbers_%d.txt' %
                 j for j in range(i*batch_size, (i+1)*batch_size)]
        filenames.append(batch)

    return filenames


def sort_files(pool_size, filenames):
    """ Sort files by batches using a multiprocessing Pool """

    with Pool(pool_size) as pool:
        counters = pool.map(sorter, filenames)

        with open('sorted_nums.txt', 'w') as fp:
            for i in range(1, MAXINT+1):
                text = str(i)+'\n'
                count = sum(x.get(text, 0) for x in counters)
                if count > 0:
                    fp.write(text*count)

        print('Sorted')


if __name__ == "__main__":
    limit = int(sys.argv[1])
    pool_size = 4

    filenames = batch_files(pool_size, limit)
    sort_files(pool_size, filenames)
