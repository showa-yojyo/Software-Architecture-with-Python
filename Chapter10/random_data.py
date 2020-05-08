#!/usr/bin/env python
# Code Listing #8
"""

Generating random data for applications - Generates random patient data

"""

import string
import random
import itertools

from schematics.models import Model
from schematics.types import BaseType, BooleanType, StringType, IntType, DecimalType, DateTimeType


class AgeType(IntType):
    """ An age type for schematics """

    def __init__(self, **kwargs):
        kwargs['default'] = 18
        super().__init__(**kwargs)

    def to_primitive(self, value, context=None):
        # 乱数を返すように見える
        return random.randrange(18, 80)

class NameType(StringType):
    """ A schematics custom name type """

    vowels = 'aeiou'
    consonants = ''.join(set(string.ascii_lowercase) - set(vowels))

    def __init__(self, **kwargs):
        kwargs['default'] = ''
        super().__init__(**kwargs)

    def get_name(self):
        """ A random name generator which generates
        names by clever placing of vowels and consontants """

        items = ['']*4

        items[0] = random.choice(self.consonants)
        items[2] = random.choice(self.consonants)

        for i in (1, 3):
            items[i] = random.choice(self.vowels)

        return ''.join(items).capitalize()

    def to_primitive(self, value, context=None):
        return self.get_name()

class GenderType(BaseType):
    """A gender type for schematics """

    def __init__(self, **kwargs):
        kwargs['choices'] = ['male', 'female']
        kwargs['default'] = 'male'
        super().__init__(**kwargs)

class ConditionType(StringType):
    """ A gender type for a health condition """

    def __init__(self, **kwargs):
        kwargs['default'] = 'cardiac'
        super().__init__(**kwargs)

    def to_primitive(self, value, context=None):
        return random.choice(('cardiac',
                              'respiratory',
                              'nasal',
                              'gynec',
                              'urinal',
                              'lungs',
                              'thyroid',
                              'tumour'))

class BloodGroupType(StringType):
    """ A blood group type for schematics  """

    def __init__(self, **kwargs):
        kwargs['default'] = 'AB+'
        super().__init__(**kwargs)

    def to_primitive(self, value, context=None):
        # random.choice() は引数がシーケンスでなければならない。
        return ''.join(random.choice(
            list(itertools.product(
                ('AB', 'A', 'O', 'B'), ('+', '-')))))


class Patient(Model):
    """ A model class for patients """

    name = NameType()
    age = AgeType()
    gender = GenderType()
    condition = ConditionType()
    doctor = NameType()
    blood_group = BloodGroupType()
    insured = BooleanType(default=True)
    last_visit = DateTimeType(default='2000-01-01T13:30:30')

if __name__ == "__main__":
     for patient in (Patient.get_mock_object().to_primitive() for _ in range(100)):
         print(patient)
