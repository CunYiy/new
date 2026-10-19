# from fileinput import close
#
# fi=open("test.txt")
# # print(fi.read())      #读取里头的文件
# # print(fi.read(4))
# print(fi.read(-4))
# print(fi.name)
# f=open(r"C:\Users\19407\Desktop\test.txt")
# print(f.name)
# while True:
#       text=fi.readline()
#       if not text:
#         break
#       print(text)
# fi.close()


# file=open('test.txt','a')    #默认r  w会覆盖原有内容  a为追加
# # print(file.read())
# file.write("\nyyy")
# file.close()

# with open("test.txt","a") as f:
#     f.write("yangcunyi")
# print(f.closed)                #判断已关闭 with open 自动关闭文件

# with open("test.txt","a",encoding="utf-8") as f:
#     f.write("\n杨存义可以娶到一个好老婆")

# with open("test.txt","r",encoding="utf-8") as f:
#     # f.write("\n杨存义可以娶到一个好老婆")
#         print(f.read())

# with open(r"C:\Users\19407\Pictures\.png","rb") as f:  #读入文件 以二进制模式b
#     img = f.read()
#     print(img)
# with open(r"C:\Users\19407\Doubao\chats\2026-10-01\new-chat\.png","wb") as f:    #将读取到的文件写入当前文件下
#     f.write(img)


import os
# os.rename("递归函数.py","递归方法-斐波那契.py")   #对源文件名进行修改
# os.remove("1.jpg")                              #删除文件
# os.mkdir("yangcunyi")                          #创建文件夹
# os.rmdir("yangcunyi")                            #删除
# get=os.getcwd()                                  #都可以用变量保存
# print(get)                                       #获得当前工作文件夹
# print(os.listdir())
print(os.listdir("../"))                          #获取上一级目录
print(os.listdir("../../"))                          #获取上上一级目录
