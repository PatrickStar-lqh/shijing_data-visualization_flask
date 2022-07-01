import pymysql
from flask import render_template, request
from . import sjdv
from .newforce import make_forcejson
from .treejson import make_treejson


@sjdv.route('/')
def word_cloud():
    conn = pymysql.connect(host='localhost',  # 服务器主机地址
                           port=3306,  # mysql数据库端口号，默认3306
                           user='root',  # 用户名
                           password='liu123456',  # 密码
                           database='chinese_poetry')  # 操作的数据库(charset，编码格式)

    # 获取游标，执行sql语句
    cursor = conn.cursor()
    sql = " select word,num from fenci where num>10 ;"
    cursor.execute(sql)
    row = cursor.fetchall()
    # 关闭游标
    cursor.close()
    # 关闭连接
    conn.close()
    print(row)
    return render_template("index.html", wordsdata=row, wordscount=len(row))

@sjdv.route('/tree_force_hist')
def tree_force_hist():
    force_url = make_forcejson()
    tree_url = make_treejson()
    return render_template("tree.html", force_url=force_url, tree_url=tree_url)

@sjdv.route('/treemap')
def treemap():
    return render_template("treemap.html", dataurl='static/jsondata/yixiang_num.json')

@sjdv.route('/pie')
def pie():
    return render_template("pie.html", dataurl='static/jsondata/yxtype_num.json')