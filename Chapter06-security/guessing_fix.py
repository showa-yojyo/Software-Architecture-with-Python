#!/usr/bin/env python
# Code Listing #2

"""

Guessing game - version two with fix

"""

import random

# Some global password information which is hard-coded
passwords = {"joe": "world123",
             "jane": "hello123"}


def game():
    """ A guessing game """

    # Use 'raw_input' to read standard input
    value = input("Please enter your guess (between 1 and 10): ")

    try:
        # str オブジェクトを int オブジェクトに変換する
        value = int(value)
    except ValueError:
        print('Wrong type entered, try again', value)
        return

    print("Entered value is", value)
    if value == random.randrange(1, 10):
        # 今度は運が良ければ 1/10 の確率で勝てる
        print("You won!")
    else:
        print("Try again")


if __name__ == "__main__":
    game()
