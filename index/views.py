#-*-coding:utf-8-*-
from django.shortcuts import render,HttpResponseRedirect,HttpResponse,render_to_response
from login.views import connect,close
from basedUserCF import adjustrecommend
#-*- coding:utf-8-*-
# Create your views here.

#猜你喜欢模块
def index(request,name):
    #连接数据库
    db,cursor = connect()
    #转换成gbk编码
    namegbk = name.encode("gbk")
    #获取当前用户的id
    sql_getid = "select userid from user where username='"+namegbk+"'"
    cursor.execute(sql_getid)
    for row in cursor.fetchall():
        uid = row[0]
    # print uid
    #获取推荐结果
    bookid_list = adjustrecommend(uid)
    # print bookid_list
    bookdic = {}
    #定义sql，提交并查询
    for bid in bookid_list:
        sql = "select * from book where bookid = '"+bid+"'"
        cursor.execute(sql)
        for row in cursor.fetchall():
            bookdic[row[1]] = {"bname":row[0].decode("gbk"),"bdisnum":row[2],"bscore":row[3]}
    close(db,cursor)
    #返回语句，带回相应的数据
    return  render_to_response("index.html",{
        "bookdic":bookdic,
        "name":name,
        "color1": "red",
        "flag":True,
    })

def hot(request,name):
    booklist = []
    #连接数据库
    db,cursor = connect()
    #定义sql，提交并查询
    sql = "select * from book"
    cursor.execute(sql)
    for row in cursor.fetchall():
        booklist.append({"bname":row[0].decode("gbk"),"bid":row[1],"bdisnum":row[2],"bscore":row[3]})
    #排序函数
    booklist = sorted(booklist,reverse=True)
    newbooklist = []
    i = 0;
    for one in booklist:
        if i<15:
            newbooklist.append(one)
            i +=1
    print i
    #返回语句，带回相应的数据
    return  render_to_response("index.html",{
        "booklist":newbooklist,
        "name":name,
        "color2": "red",
        "flag":False,
    })