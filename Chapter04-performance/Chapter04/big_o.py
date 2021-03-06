# Extra Code

"""

Big-O notation image generator. Code which generated the Big-O
growth graph (order) in the book.

"""


import math
from functools import reduce
import numpy as np
import matplotlib.pyplot as plt


def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)


def k(t):
    return [0]


def l(t):
    return [math.log(x) for x in t]


def x(t):
    return [x for x in t]


def xl(t):
    return [math.log(x)*x for x in t]


def sq(t):
    return [x*x for x in t]


def p2(t):
    return [pow(2, x) for x in t]


def fact(n):
    return reduce(lambda x, y: x*y, list(range(1, n+1)))


def facn(t):
    # XXX: 効率が悪いので本番ではこういうコードを書いてはならない
    return [fact(x) for x in t]


t = list(range(1, 101))

plt.axis([0, 50, 0, 50])
line1 = plt.plot(t, [1]*100, '#00ee00')
#print(line1)
plt.text(45, 1.5, r'$O(1)$')

line2 = plt.plot(t, l(t), color='#00bb00')
plt.text(40, 4.8, r'$O(\log n)$')

line3 = plt.plot(t, x(t), color='#008800')
plt.text(42, 40, r'$O(n)$')

line4 = plt.plot(t, xl(t), color='#eeee00')
plt.text(18, 45, r'$O(n\log n)$')

line5 = plt.plot(t, sq(t), color='#440000')
plt.text(8, 44, r'$O(n^2)$')

line6 = plt.plot(t, p2(t), color='#bb0000')
plt.text(2, 35, r'$O(2^n)$')

line7 = plt.plot(t, facn(t), color='#ff0000')
plt.text(0, 45, r'$O(n!)$')

plt.show()
