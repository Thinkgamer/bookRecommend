#-*-coding:utf-8-*-
from django.shortcuts import HttpResponseRedirect,render_to_response
import MySQLdb
from index.basedUserCF import *
from login.globalUse import *
from index.details import *
from index.views import getName
import index.details as get
from django.views.decorators.csrf import csrf_exempt


#连接数据库
def connect():
    con = MySQLdb.connect("127.0.0.1","root","root","bookrecommend",charset="utf8")
    cursor = con.cursor()
    return con,cursor
#关闭数据库
def close(db,cursor):
    db.close()
    cursor.close()

#设置当前登录用户的推荐信息
userrecommend = GlobalUse()

#登录
@csrf_exempt
def login(request):
    #提交表单时执行
    if request.method=="POST":
        #从表单获取username
        name = request.POST.get("username").encode('gbk')
        #数据库连接
        db,cursor = connect()
        #定义sql语句，并查询
        sql = "select username,userid from user"
        cursor.execute(sql)
        for row in cursor.fetchall():

            #如果存在则返回主界面
            if name==row[0].encode("gbk"):
                bookid_list,userid_list=adjustrecommend(row[1])
                userrecommend.setBookId(bookid_list)
                userrecommend.setUserId(userid_list)
                userrecommend.setSeeBook(getseeBook(row[1]))

                return HttpResponseRedirect("/index/index/%s" % row[1])
        #不存在返回login并提sta示错误
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

def center(request,uid):
    #获得相似用户列表
    uid_list=userrecommend.userid_list
    usersim_list = get.getSimUser(uid_list)

    username = getName(uid)
    return render_to_response("more.html",{
        "title":"足迹",
        "username":username,
        "uid":uid,
        "usersim_list":usersim_list,
        "book_list":userrecommend.seeBook_list,
    })


def otherCen(request,uid,otherid):
    #获得相似用户列表
    uid_list=userrecommend.userid_list
    usersim_list = get.getSimUser(uid_list)

    username = getName(uid)
    othername = getName(otherid)
    #获取otherid的读过的的书列表

    return render_to_response("more.html",{
        "title":"足迹",
        "username":username,
        "othername":othername,
        "uid":uid,
        "usersim_list":usersim_list,
        "book_list":getseeBook(otherid),
    })

def see(request):

    from index.newbook import getHotBook
    #获得hot book列表
    hotBook_list =getHotBook()
    return render_to_response("more.html",{
        "title":"随便看看",
        "book_list":hotBook_list,
    })