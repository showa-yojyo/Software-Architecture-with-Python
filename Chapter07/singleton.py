#!/usr/bin/env python
# Code Listing #4

"""

All code listings for Singleton pattern shown in the book

"""

# type を継承するときの __init__() の第一引数に注意
class MetaSingleton(type):
    """ A type for Singleton classes (overrides __call__) """

    def __init__(cls, *args):
        print(cls, "__init__ method called with args", args)
        super().__init__(*args)
        cls.instance = None

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            print(cls, "creating instance", args, kwargs)
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance

# クラス変数と __new__() を用いる実装例
class Singleton:
    """ Singleton in Python """

    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

# サブクラス子
class SingletonA(Singleton):
    pass

# サブクラス孫
class SingletonA1(SingletonA):
    pass

# サブクラス子
class SingletonB(Singleton):
    pass

# サブクラス子
class SingletonM(metaclass=MetaSingleton):
    pass


def test_single(cls):
    """ Test if passed class is a singleton """
    # Singleton パターンを意図通りに実装できているかどうかをテストするのは
    # こうすればいいのか
    return cls() == cls()


if __name__ == "__main__":
    # Check for state sharing across hierarchies

    a = SingletonA()
    a1 = SingletonA1()
    b = SingletonB()

    a.x = 100
    print(f'{a.x = }')
    print(f'{a1.x = }')
    # Will raise an exception
    try:
        print(f'{b.x = }')
    except AttributeError as e:
        # ということは SingletonA, SingletonB 同士は別 singleton を意味する。
        print('Error:', e)

    # 以下すべて True となる。
    print(test_single(Singleton))
    print(test_single(SingletonM))
    print(test_single(SingletonA))
    print(test_single(SingletonB))
    print(test_single(SingletonA1))

