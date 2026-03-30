# 第一个注释
'''
注释
注释
注释
'''
a = True
b = False
print(type(a))
print(type(b))
print(int(a))
print(int(b))
print(bool(0))
print(bool(4))
print(bool(""))
print(bool([]))
print(bool({}))
lst = [1, 2, 3, 4, 5]
print(lst[2:-4])
lst2 = [6, 7, 8]
print(lst + lst2)
sites = {'google', 'baidu', 'facebook', 'meta'}
a = set('wangyi')
b = set('ali')
print(sites)
print(a)
print(b)
for s in sites: print(s)
print(type((50)))
print(type((50,)))
print(type((0, '1', [1, 2])))

if lst[0]:
    print("1")
elif lst[1]:
    print("2")
else:
    print("3")

# number = 7
# guess = -1
# print("猜数字游戏")
# while guess != number:
#     guess = int(input("请输入你猜的数字："))1
#     if guess == number:
#         print("恭喜你猜对了")
#     elif guess < number:
#         print("猜小了")
#     else:
#         print("猜大了")


# num = int(input("请输入你的年龄"))

# match num:
#     case 6|7|8:
#         print("你是婴儿")
#     case 12:
#         print("你是小孩儿")
#     case 18:
#         print("你是成年人")
#     case 40:
#         print("你是中年")
#     case _:
#         print("你是老年")
def countdown(n):
    while n > 0:
        print("n ori:", n)
        yield n
        print("n before: ", n)
        n -= 1
        print("n after: ", n)

generator = countdown(5)
print(next(generator))
print("output 1")
print(next(generator))
print("output 2")
print(next(generator))
print("output 3")

import sys

def fibonacci(n):
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        # a, b = b, a + b
        a = b
        b = a + b
        counter += 1
f = fibonacci(10)

while True:
    try:
        print(next(f), end=" ")
    except StopIteration:
        sys.exit()