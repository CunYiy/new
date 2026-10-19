class Person():
    def __init__(self):
        print("这是初始化调用")
    def __new__(cls, *args, **kwargs):   #不重写 则自动调用object的__new__
        print("这是覆盖内存")
        print(cls)
        r=super().__new__(cls)
        return r               #r为保存变量 并返回变量的引用
person=Person()
print(person)         #此时new无法开辟新内存
# person = Person() → 调用 Person.__new__(Person)
# super().__new__(cls) 调用 object 的__new__，开辟一块内存，创建空对象，把对象引用赋值给r
# return r：把新建的空对象返回
# Python 拿到__new__返回的对象后，自动调用 __init__(r)，也就是__init__，做初始化
# 最后把__init__处理完的对象赋值给变量person
