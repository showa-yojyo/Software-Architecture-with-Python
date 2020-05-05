# Code Listing #6

"""

Objgraph example code.

Make sure you install graphviz and xdot before running this.

"""

#import pdb
import objgraph


class MyRefClass:
    pass


ref = MyRefClass()


class C:
    pass


c_objects = []
for i in range(100):
    c = C()
    c.ref = ref
    c_objects.append(c)

#pdb.set_trace()
breakpoint()

# Run this code in pdb prompt, you just need to press 'c'
objgraph.show_backrefs(ref, max_depth=2, too_many=2, filename='refs.png')
