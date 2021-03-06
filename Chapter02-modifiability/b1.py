# Code listing #11
# 標準モジュール statistics にたいていあるもの。

""" Module B (b.py) - Implement functions provide some statistical methods """

# Note - this is version 1 of b, so called b1.py

import a1 as a


def rms(narray):
    """ Return root mean square of array of numbers"""

    # cf. math.hypot()
    return pow(sum(a.squares(narray)), 0.5)


def mean(array):
    """ Return mean of an array of numbers """

    # cf. statistics.fmean()
    return 1.0*sum(array)/len(array)


def variance(array):
    """ Return variance of an array of numbers """

    # Square of variation from mean
    avg = mean(array)
    array_d = [(x - avg) for x in array]
    return sum(a.squares(array_d))


def standard_deviation(array):
    """ Return standard deviation of an array of numbers """

    # S.D is square root of variance
    return pow(variance(array), 0.5)
