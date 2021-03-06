# Code listing #9
# map() を多用しているがふつうは内包表記を用いるのが better practice だ。
# したがってそのようなコードを書き換える。

# This code calculates the sum of squares of velocities
squares = (x * x for x in varray)

# The above version is much more clearer than the version below, which uses comments
# below the code since it is keeping with the natural order of reading from top to bottom.

squares = (x * x for x in varray)
# The above code calculates the sum of squares of velocities

# Inline comments should be used very minimally
squares = (x * x for x in varray)   # Calculate squares of velocities

# Avoid superfluous comments that add little value

# The following code iterates through odd numbers
for num in nums:
    # Skip if number is odd
    if num % 2 == 0:
        continue
