#!/usr/bin/env python
# Code Listing #1
"""

Testing search of common items across two sequences

bash$ common_items.py 5000
('Time spent=>', 468.75, 'ms.')
('Time spent=>', 15.625, 'ms.')
"""

import random

from time import process_time as timer_func, sleep
from contextlib import contextmanager

# NOTE: 未使用コードを削除

# この contextmanager を使った処理時間計測関数の書き方は必修
@contextmanager
def timer():
    """ A simple timing function for routines """

    try:
        start = timer_func()
        # この yield が急所
        yield
    except Exception as e:
        print(e)
        raise
    finally:
        end = timer_func()
        print('Time spent=>{:>10.3f}ms.'.format(1000.0*(end - start)))


def common_items_v1(seq1, seq2):
    """ Find common items between two sequences - version #1 """

    common = []
    for item in seq1:
        if item in seq2:
            common.append(item)

    return common


def common_items_v2(seq1, seq2):
    """ Find common items between two sequences - optimized version (v2) """

    # return set(seq1).intersection(set(seq2))
    seq_dict1 = {item: 1 for item in seq1}
    for item in seq2:
        try:
            # collections.Counter を使うのが良さそうだ
            seq_dict1[item] += 1
        except KeyError:
            pass

    return [item[0] for item in seq_dict1.items() if item[1] > 1]


def test(n, func):
    """ Generate test data and perform test on a given function """

    stop = 2 * n
    a1 = random.sample(range(0, stop), n)
    a2 = random.sample(range(0, stop), n)

    with timer():
        func(a1, a2)


def test_():
    """ Testing the common_items function using a given input size """

    # With additional sleep
    sleep(0.01)
    common = common_items(a1, a2) # v1 or v2


if __name__ == "__main__":
    import sys
    n = int(sys.argv[1])
    test(n, common_items_v1)
    test(n, common_items_v2)
