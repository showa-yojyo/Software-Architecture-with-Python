#!/usr/bin/env python
# Code Listing #3

"""

Code testing the 'eval' function for security holes

"""

# test_eval.py
import sys
import os # 不用意に import する


def run_code(string):
    """ Evaluate the passed string as code """

    try:
        # globals={} により安全になったかと思われるが、そうではない。
        # Python には __import__() が存在する。
        # E.g. string="__import__('os').system('rm -rf /')"
        eval(string, {})
    except Exception as e:
        print(repr(e))


if __name__ == "__main__":
    run_code(sys.argv[1])
