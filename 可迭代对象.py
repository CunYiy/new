from collections.abc import Iterable,Iterator    #abc是一个内置模块 命名不能重复
# print(isinstance("avvkk",Iterable))
# print(isinstance(263,int))
# print(isinstance((1,2,3),Iterable))
# for i in [3,43,56,57,4,77]:
#     print(i)                  #利用for循环依次取出
# li = (1,224,55,675,878)
# li1=iter(li)                  #li1被变成迭代器
# print("li1为对象,其地址为:",li1)
# print(next(li1))
# print(next(li1))
# print(next(li1))
# print(next(li1))              #本质为魔法方法
# print(isinstance("avvkk",Iterable))
# # print(isinstance("avvkk",Iterator))
# li=[i*5+1 for i in range(9)]        #计算式返回一个列表
# print(li)
# gen=(i*5+1 for i in range(9))      #[]-()由列表推导式变为生成器
# print(gen)                         #生成器对象
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))
# print(next(gen))                    #自定义生成器可调用next()

def gen_1():
    yield 2
    yield 4
    yield 6
    yield 8
print(gen_1())                       #使用yield变为生成器
print(next(gen_1()))
print(next(gen_1()))
print(next(gen_1()))
print(next(gen_1()))