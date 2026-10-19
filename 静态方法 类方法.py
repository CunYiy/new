# class Student():
#     @staticmethod         #定义一个静态方法
#     def PlayGame(name):
#         print(f"{name}学生会偷偷在宿舍打游戏")
# student=Student()
# Student().PlayGame("yangcunyi")
# student.PlayGame("yangcunyi")        #静态方法可以由类名和实例对象调用  也可实参传递
class Student(object):
    name="yangcunyi"
    @classmethod            #类方法
    def Sing(cls):          #cls代表类本身
        print("学生会唱歌")
        print(cls.name)
student=Student()
student.Sing()

