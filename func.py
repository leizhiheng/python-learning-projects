def hello():
    print("Hello world!")

hello()

def print_info(name, age = 15):
    print("name: ", name)
    print("age: ", age)

print_info("lzh", 20)

def print_info2(arg1, *vartuple):
    print("arg1: ", arg1)
    print("var tuple: ", vartuple)

print_info2("lzh", 60, 70, 80, 90)

def print_info3(arg1, **vardict):
    print("arg1: ", arg1)
    print("vardict:", vardict)
print_info3("blue", a = 10, b = "20")

f  = lambda: "Hello world"
print(f())
x = lambda a: a + 10
print(x(10))
numbers = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x**2, numbers))
print(squared)
print(list)
print(type(list))
print(type(numbers))
print(map)
print(type(map))
print(type({}))

even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

from functools import reduce
product = reduce(lambda x, y: x * y, numbers)
print(product)