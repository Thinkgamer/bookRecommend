#-*-coding:utf-8-*-
from django.shortcuts import HttpResponseRedirect,render_to_response
import MySQLdb
from index.basedUserCF import *
from login.globalUse import *
from index.details import *
from index.views import getName
import index.details as get
import random
from index.basedItem import recommend
from django.views.decorators.csrf import csrf_exempt


#连接数据库
def connect():
    con = MySQLdb.connect("127.0.0.1","root","root","bookrecommend",charset="utf8")
    cursor = con.cursor()
    return con,cursor
#关闭数据库
def close(db,cursor):
    db.commit()
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
                try:
                    bookid_list,userid_list=adjustrecommend(row[1])
                    itembook_list =recommend(row[1])
                except:
                    from coldstart import coldstart,getItemBook
                    bookid_list,userid_list=coldstart(row[1])
                    itembook_list =getItemBook(bookid_list)
                userrecommend.setBookId(bookid_list)
                userrecommend.setUserId(userid_list)
                userrecommend.setSeeBook(getseeBook(row[1]))
                userrecommend.setItemBook(itembook_list)

                return HttpResponseRedirect("/index/index/%s" % row[1])
        #不存在返回login并提sta示错误
        return render_to_response("login.html",{
            'error':"你输入的用户不存在，请重新输入",
        })
    #浏览器访问时执行
    else:
        return render_to_response("login.html",{ })

#用户注册
@csrf_exempt
def regeister(request):

    if request.method == "POST":
        db,cursor = connect()  #数据库连接
        name = request.POST.get("username") #获取用户名
        year = request.POST.get("year") #获取出生年月
        job = request.POST.get("ujob")     #获取job
        sex = request.POST.get("sex")
        import time
        uid = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        sql = "insert into user values(%s,%s,%s,%s,%s,%s)"
        arr = (uid,name,"root",year,job,sex)
        cursor.execute(sql,arr)
        close(db,cursor)
        from coldstart import coldstart,getItemBook
        bookid_list,userid_list=coldstart(uid)
        itembook_list =getItemBook(bookid_list)
        userrecommend.setBookId(bookid_list)
        userrecommend.setUserId(userid_list)
        userrecommend.setSeeBook(getseeBook(row[1]))
        userrecommend.setItemBook(itembook_list)

        return HttpResponseRedirect("/login/see/%s" % uid)
    return render_to_response("regeister.html",{

    })

def center(request,uid):
    #获得相似用户列表
    uid_list=userrecommend.userid_list
    usersim_list = get.getSimUser(uid_list)

    #更新看过的书
    userrecommend.setSeeBook(getseeBook(uid))

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

def see(request,uid):
    username = getName(uid)
    from index.newbook import getHotBook
    #获得hot book列表
    hotBook_list =getHotBook()
    return render_to_response("see.html",{
        "book_list":hotBook_list,
        "uid":uid,
        "username":username
    })