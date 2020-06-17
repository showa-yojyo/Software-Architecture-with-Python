# Code Listing - #9
# Docstring 内の記述を doctest する実演コード。

"""
Module factorial - Demonstrating an example of writing doctests
"""

import functools
import operator


def factorial(n):
    """ Factorial of a number.

    >>> factorial(0)
    1
    >>> factorial(1)
    1
    >>> factorial(5)
    120
    >>> factorial(10)
    3628800
    """

    # Handle 0 as a special case
    if n == 0:
        return 1

    # この階乗の実装は再帰呼び出しを避けているので OK だ。
    # なお Python 3.8 なら math.prod(range(1, n + 1), 1) でいい。上の if 文もいらない。
    return functools.reduce(operator.mul, list(range(1, n+1)))


if __name__ == "__main__":
    # doctest.testfile('factorial.py') もしくは
    # python -m doctest -v factorial.py としてもテスト可能。
    import doctest
    doctest.testmod(verbose=True)
