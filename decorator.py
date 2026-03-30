# 装饰器是 Python 的一种高级功能，它允许你动态地修改函数或者类的行为
# 装饰器本质上是一个函数，接受一个函数作为参数并返回一个新的包装过后的函数对象
# 语法使用 @decorator_name 来应用在函数或者类上

# ===== 1. 最简单的装饰器示例 =====
def my_decorator(func):
    """一个简单的装饰器"""
    def wrapper():
        print("函数执行前...")
        func()
        print("函数执行后...")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

# 调用
say_hello()

def my_decorator2(func):
    def wrapper(*args, **kwargs):
        print("函数执行前")
        result = func(*args, **kwargs)
        print("函数执行后")
        return result
    return wrapper


@my_decorator2
def add(a, b):
    return a + b

print(f"result: {add(10, 20)}")

print(f"模块的__name__ : {__name__}")



import hello



