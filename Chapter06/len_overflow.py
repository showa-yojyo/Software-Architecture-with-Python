#!/usr/bin/env python
# Code Listing #5

"""

Code testing the 'len' function for overflow errors

"""


class A:
    def __len__(self):
        return 100 ** 100


class B:
    def __len__(self):
        return 100 ** 100


try:
    len(A())
    print("""OK: 'class A with 'return 100 ** 100' - len calculated""")
except Exception as e:
    print(type(e))
    print("""Not OK: 'class A' with 'return 100 ** 100' - len raise Error: """ + repr(e))

try:
    len(B())
    print("""OK: 'class B' with 'return 100 ** 100' - len calculated""")
except Exception as e:
    print(type(e))
    print("""Not OK: 'class B' with 'return 100 ** 100' - len raise Error: """ + repr(e))
