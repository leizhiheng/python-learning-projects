print(str("Start input"))

f = open("./writefile.txt", "w")
num = f.write("python是一个非常好的语言。\n是的，的确非常好\n")
print(num)
f.close()

f = open("./writefile.txt", "r")
# str = f.read()
# str = f.readlines()
for line in f:
    print(line, end=" ")
print(str)
print(f.isatty())

import os

cur_directory = os.getcwd()
print("cur direct: ", cur_directory)
# os.chdir("./..")
# print("新的工作目录：", os.getcwd())
print("目录内容：", os.listdir())

os.rmdir("testdirect")
os.mkdir("testdirect")
os.chdir("./testdirect")

print("目录：", os.getcwd())

while True:
    try:
        x = int(input("请输入一个数字："))
        break
    except ValueError as err:
        print("输入的不是数字！, error:", err)