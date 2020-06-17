# Code listing #8
# math.sqrt(x) の代わりに pow(x, 0.5) というのは面白い。
# Python 3.8 なら math.dist(varray) でいいだろう。


def rms(varray):
    """ Root mean squared velocity. Returns
    square root of sum of squares of velocities """

    return pow(sum(x**2 for x in varray), 0.5)
