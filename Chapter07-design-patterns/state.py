#!/usr/bin/env python
# Code Listing #16
"""

State pattern - Using a computer and its state as an example.
The implementation technique uses an iterator.

"""

import random
import itertools

class IllegalStateTransition(Exception):
    pass

# State かつ Iterator
class ComputerState:
    """ Base class for state of a computer """

    # This is an iterator
    name = "state"
    next_states = []
    random_states = []

    def __init__(self):
        self.index = 0

    def __str__(self):
        return self.__class__.__name__

    def __iter__(self):
        return self

    def change(self):
        # たぶん __next__() のコードを本メソッドの定義として、
        # __next__() の定義は self.change() とするのが好み。
        return self.__next__()

    def set(self, state):
        """ Set a state """

        if self.index < len(self.next_states):
            # 合法な状態遷移
            if state in self.next_states:
                # Set index
                self.index = self.next_states.index(state)
                self.__class__ = eval(state) # 刺激的なコード
                return self.__class__
            else:
                # Raise an exception for invalid state change
                current = self.__class__.__name__
                raise IllegalStateTransition(
                    'Illegal transition from %s to %s' % (current, state))
        else:
            # ランダムに状態を決めることにする
            self.index = 0
            if state in self.random_states:
                self.__class__ = eval(state) # 刺激的なコード
                return self.__class__

    def __next__(self):
        """ Switch to next state """

        if self.index < len(self.next_states):
            # Always move to next state first
            self.__class__ = eval(self.next_states[self.index]) # 刺激的なコード
            # Keep track of the iterator position
            self.index += 1
            return self.__class__
        else:
            # Can switch to a random state once it completes
            # list of mandatory next states.

            # Reset index
            self.index = 0
            if len(self.random_states):
                state = random.choice(self.random_states)
                self.__class__ = eval(state) # 刺激的なコード
                return self.__class__
            else:
                raise StopIteration

# 以下 ConcreteState クラス群。
# クラス変数に注意（オブジェクト化しないで利用することがわかる）
# 文字列でクラス名を取り扱和ざるを得ない。

class ComputerOff(ComputerState):
    next_states = ['ComputerOn']
    random_states = ['ComputerSuspend', 'ComputerHibernate', 'ComputerOff']


class ComputerOn(ComputerState):
    random_states = ['ComputerSuspend', 'ComputerHibernate', 'ComputerOff']


class ComputerWakeUp(ComputerState):
    random_states = ['ComputerSuspend', 'ComputerHibernate', 'ComputerOff']


class ComputerSuspend(ComputerState):
    next_states = ['ComputerWakeUp']
    random_states = ['ComputerSuspend', 'ComputerHibernate', 'ComputerOff']


class ComputerHibernate(ComputerState):
    next_states = ['ComputerOn']
    random_states = ['ComputerSuspend', 'ComputerHibernate', 'ComputerOff']


class Computer:
    """ A class representing a computer """

    def __init__(self, model):
        self.model = model
        # State of the computer - default is off.
        self.state = ComputerOff()

    def change(self, state=None):
        """ Change state """

        if not state:
            return self.state.change()
        else:
            return self.state.set(state)

    def __str__(self):
        """ Return state """
        return str(self.state)


if __name__ == "__main__":
    c = Computer('ASUS')
    print(c)

    print(c.change())
    print(c.change('ComputerHibernate'))

    # Now since this is an iterator we can even loop it
    print('Iterating')

    for s in itertools.islice(c.state, 5):
        print(s)

    # Switch off
    print(c.change('ComputerOff'))
    print(c.change('ComputerOn'))
    print(c.change('ComputerSuspend'))
    # Will raise an exception!
    print(c.change('ComputerHibernate'))
