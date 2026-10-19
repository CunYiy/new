class person(object):
    obj=None
    def __new__(cls, *args, **kwargs):
        print("这是__new__方法")
        if cls.obj==None:
            cls.obj = super().__new__(cls)   #第一次为空 指向内存分配地址
        return cls.obj                       #若不为空 则返回obj此时所在地址
    def __init__(self):
        print("这是__init__方法")
pe1=person()
print(pe1)
pe2=person()
print(pe2)      #单例模式
pe3=person()
print(pe3)      #多少个都会返回一个已分配地址
