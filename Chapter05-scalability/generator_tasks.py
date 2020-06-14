# Code Listing #11

"""

Simple example of co-operative multitasking scheduler using generators

"""

# generator_scheduler.py
from contextlib import contextmanager
import time
import collections

# yield するだけでコルーチン呼ばわりできるか
def number_generator(n):
    """ A co-routine that generates numbers in range 1..n """

    for i in range(1, n+1):
        yield i


def square_mapper(numbers):
    """ A co-routine task for converting numbers to squares """

    for n in numbers:
        yield n*n


def prime_filter(numbers):
    """ A co-routine which yields prime numbers """

    primes = []
    for n in numbers:
        if n % 2 == 0:
            continue
        flag = True
        for i in range(3, int(n**0.5+1), 2):
            if n % i == 0:
                flag = False
                break

        if flag:
            yield n


def scheduler(tasks, runs=10000):
    """ Basic task scheduler for co-routines """

    results = collections.defaultdict(list)

    for i in range(runs):
        for t in tasks:
            print('Switching to task', t.__name__)
            try:
                result = next(t)
                print(f'{result=}')
                results[t.__name__].append(result)
            except StopIteration:
                break

    return results

# 復習
@contextmanager
def timer():
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('Time taken=>', end - start)

if __name__ == "__main__":
    import sys
    tasks = []
    limit = int(sys.argv[1])

    with timer():
        tasks.append(square_mapper(number_generator(limit)))
        tasks.append(prime_filter(number_generator(limit)))

        results = scheduler(tasks, runs=limit)
        print('Last prime=>', results['prime_filter'][-1])
