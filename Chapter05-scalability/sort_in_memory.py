# Code Listing #8
# これは意味がわからない。
"""

Sort a number of disk files in memory - using normal list sort

"""

import sys


def sort():
    all_lists = []

    for i in range(int(sys.argv[1])):
        with open('numbers/numbers_%d.txt' % i) as f:
            all_lists += [int(line) for line in f.readlines()]

    print('Length of list', len(all_lists))
    print('Sorting...')
    all_lists.sort()
    with open('sorted_nums.txt', 'w') as f:
        f.writelines('\n'.join(str(n) for n in all_lists) + '\n')
    print('Sorted')


if __name__ == "__main__":
    sort()
