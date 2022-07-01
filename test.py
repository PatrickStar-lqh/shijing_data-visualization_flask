import pymysql
import json
#创建连接对象 connect=Connection=Connect 都可以创建一个连接对象
conn = pymysql.connect(host='localhost',#服务器主机地址
                       port=3306,#mysql数据库端口号，默认3306
                       user='root',#用户名
                       password='liu123456',#密码
                       database='chinese_poetry')#操作的数据库(charset，编码格式)

#获取游标，执行sql语句
cursor = conn.cursor()
sql = " select word,num from fenci where num>10 ;"
cursor.execute(sql)
row=cursor.fetchall()
fencidata=[]
for i in row:
    fencidata.append({'text':i[0],'num':i[1]})
print(fencidata)
#关闭游标
cursor.close()
#关闭连接
conn.close()