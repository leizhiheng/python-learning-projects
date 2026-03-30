class People:
    name = ''
    age = 0
    __weight = 0

    def __init__(self, n, a, w):
        self.name = n
        self.age = a
        self.__weight = w
    def speak(self):
        print("%s 说： 我%d岁。" %(self.name, self.age))

class Student(People):
    def __init__(self, n, a, w, g):
        super().__init__(n, a, w)
        self.grade = g
    def speak(self):
        print("%s 说：我%d岁了，读%d年纪。" %(self.name, self.age, self.grade))

s = Student("lzh", 23, 30, 6)
s.speak()

a = 10
b = 20
def test():
    global a, b
    a = 40
    b = 50
    print("a: %d b: %d" %(a, b))

test()
print("a: %d b: %d" %(a, b))