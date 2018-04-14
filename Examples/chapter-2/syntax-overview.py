
# Everything after the # symbol is a comment
"""
Block comments in Python are between 3 double-quotes.
"""

# define a variable and assign zero to it
a = 0

# function
def say_hello():
    return "Saying Hello"


# call the function and print the result
print(say_hello())

# function with parameters
def do_sum(a, b):
    return a + b

print("a+b = {}".format(do_sum(5, 3)))

# if and comparers
a = 5
b = 10

if a == b:
    print("a equals b")    # will not be executed
elif a < b:
    print("a equals b")    # will be executed
else:
    print("a >= b")    # will not be executed


# FOR iterator
# 'i' will hold the current values
# Range function expects 3 params: start, stop and optionally step
for i in range(0, 10, 2):
    # will print 0, 2, 4, 6, 8
    print(i, end="-")
