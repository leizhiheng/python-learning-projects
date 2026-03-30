

def greet():
    print("来自 example 模块的问候！")

if __name__ == "__main__":
    print("该hello脚本正在直接运行")
else:
    print(f"该hello脚本作为模块导入, name: {__name__}")