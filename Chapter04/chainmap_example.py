# Code Listing #10

"""

Example of using ChainMap

"""

from collections import ChainMap

d1 = {i: i for i in range(100)}
d2 = {i: i*i for i in range(100)}
c = ChainMap(d1, d2)
# Older value still accessible
print(c[5]) # 5
print(c.maps[0][5]) # 5
# Updating d1 with d2
d1.update(d2)
print(d1) # 内容としては d1 == d2
# Olde value got updated
print(c[5]) # 25
print(c.maps[0][5]) # 25

# ChainMap は二つの dict を緩く結合しているのだろう。
