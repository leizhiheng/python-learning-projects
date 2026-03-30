# num1 = input("请输入第一个数字：")
# num2 = input("请输入第二个数字：")
# sum = float(num1) + float(num2)
# print("数字 {0} 和 数字 {1} 的和为：{2}".format(num1, num2, sum))

# num = float(input("请输入一个数字："))
# num_sqrt = num ** 0.5
# print("%0.3f 的平方根为：%0.3f" %(num, num_sqrt))

import cmath

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except:
            print("请输入有效的数字！")

# 二次方程
def solve_quadratic(a, b, c):
    discriminant = b ** 2 - 4*a*c
    root1 = (-b - cmath.sqrt(discriminant)) / (2 * a)
    root2 = (-b + cmath.sqrt(discriminant)) / (2 * a)
    return root1, root2

def solve_quadratic_test():
    print("求解二次方程 ax^2 + bx + c = 0")
    a = get_float_input("请输入二次项系数 a (a ≠ 0)： ")
    while a == 0:
        print("二次方程二次项系数a不能为0！")
        a = get_float_input("请输入二次项系数 a (a ≠ 0)： ")
    
    b = get_float_input("请输入一次项系数 b: ")
    c = get_float_input("请输入常数项 c: ")
    
    root1, root2 = solve_quadratic(a, b, c)
    print(f"方程解为{root1}和{root2}")

# 三角形面积
def triangle_area():
    a = get_float_input("请输入三角形第一边长:")
    b = get_float_input("请输入三角形第二边长:")
    c = get_float_input("请输入三角形第三边长:")
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    print("三角形面积为：%0.2f" %area)

from math import pi
# 计算圆的面积
def cycleArea():
    r = get_float_input("请输入圆的半径：")
    area = pi * (r ** 2)
    print("圆的面积为：%0.2f" %area)

import random
# 随机数生成
def randomNum():
    print("生成0.0~1.0之间的小数：%0.2f" %(random.random()))
    print("生成0到100之间的整数：%d" %(random.randint(0, 100)))
    li = [1, 2, 3, 4, 5]
    print("从列表中随机选择一个数：%d" %(random.choice(li)))
    random.shuffle(li)
    print("将列表进行随机排序：", li)

# 摄氏度转华氏度
def celsius_convert():
    c = get_float_input("输入摄氏温度：")
    fahrenheit = (c * 1.8) + 32
    print("%0.1f 摄氏度转为华氏度温度为：%0.1f" %(c, fahrenheit))

# 交换变量
def exchange_var():
    x = get_float_input("输入 x 值：")
    y = get_float_input("输入 y 值：")
    temp = x
    x = y 
    y = temp
    print("交换后 x 的值为：{}".format(x))
    print("交换后 y 的值为：{}".format(y))

def if_use():
    a = get_float_input("请输入一个数字：")
    if a > 0:
        print("输入的数 {} 是正数".format(a))
    elif a == 0:
        print("输入的数 {} 是零".format(a))
    else:
        print("输入的数 {} 是负数".format(a))


def main():
    # solve_quadratic_test()
    # triangle_area()
    # cycleArea()
    # randomNum()
    # celsius_convert()
    # exchange_var()
    if_use()


if __name__ == "__main__":
    main()

