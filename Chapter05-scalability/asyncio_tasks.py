#!/usr/bin/env python
# Code Listing #12
"""

Example of co-operative multitasking using asyncio

"""

import asyncio

# ジェネレーター
def number_generator(m, n):
    """ A number generator co-routine in range(m...n+1) """
    yield from range(m, n+1)


async def prime_filter(m, n):
    """ Prime number co-routine """

    primes = []
    for i in number_generator(m, n):
        if i % 2 == 0:
            continue
        flag = True

        for j in range(3, int(i**0.5+1), 2):
            if i % j == 0:
                flag = False
                break

        if flag:
            print('Prime=>', i)
            primes.append(i)

        # At this point the co-routine suspends execution
        # so that another co-routine can be scheduled.
        await asyncio.sleep(1.0)

    return primes


async def square_mapper(m, n):
    """ Square mapper co-routine """

    squares = []

    for i in number_generator(m, n):
        print('Square=>', i*i)
        squares.append(i*i)

        # At this point the co-routine suspends execution
        # so that another co-routine can be scheduled.
        await asyncio.sleep(1.0)

    return squares


def print_result(future):
    print('Result=>', future.result())


# この非同期処理は基本形。挙動が予測しやすい。
async def main():
    m, n = 10, 50
    future = asyncio.gather(
        prime_filter(m, n), square_mapper(m, n))
    future.add_done_callback(print_result)
    await future

asyncio.run(main())
