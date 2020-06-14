#!/usr/bin/env python
# Code Listing #5

"""

Borg - Pattern which allows class instances to share state without the strict requirement
of Singletons

"""


class Borg:
    """ I ain't a Singleton """
    # クラス変数として dict を持つ
    __shared_state = {}

    def __init__(self):
        self.__dict__ = self.__shared_state

# サブクラス子
class IBorg(Borg):
    """ I am a Borg """

    def __init__(self):
        super().__init__()
        self.state = 'init'

    def __str__(self):
        return self.state

# サブクラス孫 1
class ABorg(Borg):
    pass

# サブクラス孫 2
class BBorg(Borg):
    pass

# サブクラスひ孫
class A1Borg(ABorg):
    pass


if __name__ == "__main__":
    a = ABorg()
    a1 = A1Borg()
    b = BBorg()

    a.x = 100
    # すべて 100 を出力する。
    print(f'{a.x = }')
    print(f'{a1.x = }')
    print(f'{b.x = }')
