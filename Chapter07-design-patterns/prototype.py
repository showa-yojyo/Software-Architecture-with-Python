#!/usr/bin/env python
# Code Listing #7
"""

Protype design pattern and related classes

"""


import copy
from borg import Borg # 再利用も大事だ

# type から派生したクラス
class MetaPrototype(type):
    """ A metaclass for Prototypes """

    def __init__(cls, *args):
        super().__init__(*args)
        cls.clone = lambda self: copy.deepcopy(self)


class MetaSingletonPrototype(type):
    """ A metaclass for Singleton & Prototype patterns """

    def __init__(cls, *args):
        # main までにここに来ることに注意
        print(cls, "__init__ method called with args", args)
        super().__init__(*args)
        cls.instance = None
        cls.clone = lambda self: copy.deepcopy(cls.instance)

    def __call__(cls, *args, **kwargs):
        if not cls.instance:
            print(cls, "creating prototypical instance", args, kwargs)
            cls.instance = super().__call__(*args, **kwargs)
        return cls.instance

# サブクラス子
class PrototypeM(metaclass=MetaSingletonPrototype):
    """ Top-level prototype class using MetaSingletonPrototype """
    pass

# サブクラス孫
class ItemCollection(PrototypeM):
    """ An item collection class """

    def __init__(self, items=[]):
        self.items = items

# 以下、別系統のクラス群定義

class Prototype:
    """ A prototype base class """

    def clone(self):
        """ Return a clone of self """
        return copy.deepcopy(self)

# サブクラス
class Register(Prototype):
    """ A student Register class  """

    def __init__(self, names=[]):
        self.names = names

# ディープでないコピー
class SPrototype:
    """ A prototype base class using shallow copy """

    def clone(self):
        """ Return a clone of self """
        return copy.copy(self)

# サブクラス 1
class SRegister(SPrototype):
    """ Sub-class of SPrototype """

    def __init__(self, stuff=(), names=[]):
        self.stuff = stuff
        self.names = names

# サブクラス 2
class Name(SPrototype):
    """ A class representing a person's name """

    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __str__(self):
        return ' '.join((self.first, self.second))

# サブクラス 3
class Animal(SPrototype):
    """ A class representing an animal """

    def __init__(self, name, type='Wild'):
        self.name = name
        self.type = type

    def __str__(self):
        return ' '.join((str(self.type), self.name))

# サブクラス 4
class Address(SPrototype):
    """ An address class """

    def __init__(self, building, street, city, zip, country):
        self.building = building
        self.street = street
        self. city = city
        self.zip = zip
        self.country = country

    def __str__(self):
        return ', '.join((list(map(str, (self.building, self.street, self.city, self.zip, self.country)))))


# Singleton 風クラスからの派生
class PrototypeFactory(Borg):
    """ A Prototype factory/registry class """

    def __init__(self):
        """ Initializer """

        self._registry = {}

    def register(self, instance):
        """ Register a given instance """

        # {型: オブジェクト}
        self._registry[instance.__class__] = instance

    def clone(self, klass):
        """ Return cloned instance of given class """

        instance = self._registry.get(klass)
        if not instance:
            print('Error:', klass, 'not registered')
        else:
            return instance.clone()


if __name__ == "__main__":
    r1 = Register(names=['amy', 'stu', 'jack'])
    r2 = r1.clone()
    print(r1) # Register object at xxxxx
    print(r2) # Register object at yyyyy
    print(r1 == r2) # 値は同じだが False

    r1 = SRegister(names=['amy', 'stu', 'jack'])
    r2 = r1.clone()

    r1.names.append('bob')
    print(f'{r1.names == r2.names = }') # True
    print(f'{r1.names is r2.names = }') # True

    i1 = ItemCollection(items=['apples', 'grapes', 'oranges'])
    # 'ItemCollection creating prototypycal...' が出力
    print(i1) # ItemCollection object at
    # Invokes the Prototype API
    i2 = i1.clone()
    print(f'{i1.items is i2.items = }') # False
    # Invokes the Singleton API
    i3 = ItemCollection(items=['apples', 'grapes', 'oranges'])
    print(f'{i1 is i3 = }') # True

    # Illustrating factory
    name = Name('Bill', 'Bryson')
    animal = Animal('Elephant')
    factory = PrototypeFactory()

    factory.register(animal)
    factory.register(name)

    # Clone them

    name2 = factory.clone(Name)
    animal2 = factory.clone(Animal)

    print(name, name2) # Bill Bryson Bill Bryson
    print(animal, animal2) # Wild Elephant Wild Elephant

    print(f'{name is not name2 = }') # True
    print(f'{animal is not animal2 = }') # True

    class C:
        pass

    # register() していないと clone() できないことを示す：
    factory.clone(C) # Error: C not registered
