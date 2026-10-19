class Amaml(object):
    def run(self):
        print("所有动物都会跑")
    def eat(self):
        print("吃饭长大")
class cat(Amaml):
    def beit(self):
        print("猫会咬人 所以其为派生类")
    def Taimao(self):
        print("触发舔毛代码")
    def run(self):
        print("小猫飞快的跑")
# ca=cat()
# ca.beit()
#多继承调用
class Tiger(cat):
    def hunt(self):
        print("会捕猎")
    def run(self):
        print("老虎猛冲")
ti=Tiger()
# ti.beit()
# ti.eat()
# ti.hunt()
# print(Tiger.__mro__)
# ti.run()
# ca=cat()
# ca.run()       #类中不同形态 多态
def test(obj):
    obj.run()
an=Amaml()
ca=cat()
ti=Tiger()
test(an)
test(ca)
test(ti)         #以传参数的形式来体现多态

