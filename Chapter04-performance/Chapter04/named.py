# Code Listing #11

"""

Example of using namedtuple

"""

from collections import namedtuple

Employee = namedtuple('Employee', 'name, age, gender, title, department')
print(Employee)
# Create an employee
jack = Employee('Jack', 25, 'M', 'Programmer', 'Engineering')
print(jack)

# namedtuple は iterable である
for field in jack:
    print(field)

# This will raise an error
# jack.age=32
# namedtuple は immutable なので、データ編集用途には不向きだ。

# This works fine
# これは知らなかった。
print(jack._replace(age=32))
