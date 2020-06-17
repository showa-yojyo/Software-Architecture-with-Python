# Code listing #23


def factorial(n):
    """ Return factorial of n """
    if n == 0:
        return 1
    else:
        return n*factorial(n-1)

# これは再帰関数の概念を説明するためだけのコードと考えたい。
# 階乗計算を再帰で実装してはならない。
