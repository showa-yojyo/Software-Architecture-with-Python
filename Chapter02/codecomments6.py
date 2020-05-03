# Code listing #8
# math.sqrt(x) の代わりに pow(x, 0.5) というのは面白い。
# Python 3.8 なら math.dist(varray) でいいだろう。


def rms(varray=[]):
    """ Root mean squared velocity. Returns
    square root of sum of squares of velocities """

    squares = map(lambda x: x*x, varray)
    return pow(sum(squares), 0.5)

