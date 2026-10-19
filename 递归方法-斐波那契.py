# def sm():
#     a=0
#     for i in range(1,102):
#         a+=i
#     print(a)
# sm()               #利用普通函数计算求和
#
# def DiGui(n):
#     if n==1:
#         return 1          #如果n=1 跳出递归得1 得到100!
#     return n*DiGui(n-1)
# print(DiGui(100))

def fi(m):
    if m<=1:           #这里其实是0和1
        return m
    return fi(m-1)+fi(m-2)   #斐波那契数列求和
print(fi(16))             #递归深层费时间 数据不宜过大