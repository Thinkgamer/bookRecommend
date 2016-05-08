#-*-coding:utf-8-*-
from django.shortcuts import render,HttpResponseRedirect,render_to_response
import MySQLdb
from django.views.decorators.csrf import csrf_exempt

#连接数据库
def connect():
    con = MySQLdb.connect("127.0.0.1","root","root","bookrecommend")
    cursor = con.cursor()
    return con,cursor
#关闭数据库
def close(db,cursor):
    db.close()
    cursor.close()
#登录
@csrf_exempt
def login(request):
    #提交表单时执行
    if request.method=="POST":
        #从表单获取username
        name = request.POST.get("username")
        #数据库连接
        db,cursor = connect()
        #定义sql语句，并查询
        # print len(name.encode('gbk'))
        sql = "select username from user"
        cursor.execute(sql)
        # print cursor.execute(sql)
        for row in cursor.fetchall():
            # print len(row[0])
            #如果存在则返回主界面
            if name.encode('gbk')==row[0]:
                return HttpResponseRedirect("/index/index/%s" % name)
        #不存在fanhuilogin并提sta示错误
        return render_to_response("login.html",{
            'error':"你输入的用户不存在，请重新输入",
        })
    #浏览器访问时执行
    else:
        return render_to_response("login.html",{ })

def see(request):
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
    for one in booklist:
        newbooklist.append(one)
    #返回语句，带回相应的数据
    return  render_to_response("see.html",{
        "booklist":newbooklist,
    })