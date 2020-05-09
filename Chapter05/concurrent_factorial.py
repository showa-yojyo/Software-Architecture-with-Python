#!/usr/bin/env python
# Code Listing #15
"""

Factorial of numbers using concurrent futures.

"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import math


def factorial(n):
    return math.prod(range(1, n + 1))


with ThreadPoolExecutor(max_workers=2) as executor:
    future_map = {executor.submit(factorial, n): n for n in range(10, 21)}
    # 意外な順序で表示されるかもしれない。
    for future in as_completed(future_map):
        print(f'Factorial of {future_map[future]} is {future.result()}')
