# Code Listing #15

"""

Factorial of numbers using concurrent futures.

"""

from concurrent.futures import ThreadPoolExecutor, as_completed
#import functools
#import operator
import math


def factorial(n):
    #return functools.reduce(operator.mul, [i for i in range(1, n+1)])
    return math.prod(range(1, n + 1))


with ThreadPoolExecutor(max_workers=2) as executor:
    future_map = {executor.submit(factorial, n): n for n in range(10, 21)}
    # 意外な順序で表示されるかもしれない。
    for future in as_completed(future_map):
        num = future_map[future]
        print(f'Factorial of {num} is {future.result()}')
