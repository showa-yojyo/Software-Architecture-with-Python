#!/usr/bin/env python
# Code Listing #1

"""

Guessing game - version one

"""

import random

# Some global password information which is hard-coded
passwords = {"joe": "world123",
             "jane": "hello123"}


def game():
    """ A guessing game """

    # Use 'input' to read standard input
    value = input("Please enter your guess (between 1 and 10): ")

    print("Entered value is", value)
    if value == random.randrange(1, 10):
        print("You won!")
    else:
        # input() の返り値は str オブジェクトにつきここにしか来ない
        print("Try again")


if __name__ == "__main__":
    game()
