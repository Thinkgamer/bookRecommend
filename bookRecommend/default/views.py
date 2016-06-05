#-*-coding:utf-8-*-
from django.shortcuts import render_to_response,HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from login.views import connect,close
from django.template import loader,Context
# Create your views here.

def admin(request,name):
    return HttpResponseRedirect("/default/amanage/%s" % name)

@csrf_exempt
def login(request):
    if request.method=="POST":
        name = request.POST.get("username")
        pwd = request.POST.get("password")

        db,cursor = connect()
        sql = "select * from adminuser where username='"+name+"' and userpwd='"+pwd+"' "
        if cursor.execute(sql):
            close(db,cursor)
            return HttpResponseRedirect("/default/admin/%s" % name)
        else:
            close(db,cursor)
            return render_to_response("adminlogin.html", {
                "error":"账号或者密码不正确",
            })

    return render_to_response("adminlogin.html",{

    })

#用户管理上一页
def umanago(request,admin,num=1):
    title = "用户管理"
    user_list = []
    num = int(num)
    if num==1:
        num = 1
    else:
        num = int(num) - 1
    db,cursor = connect()
    sql = "select * from user ORDER BY -userborth"
    cursor.execute(sql)
    for row in cursor.fetchall():
        user_list.append({"uid":row[0],"uname":row[1],"upwd":row[2],"uborth":row[3],"ujob":row[4],"usex":row[5]})
    close(db,cursor)
    return render_to_response("admin.html",{
        "title":title,
        "name":admin,
        "user_list":user_list[(int(num)-1) * 14:int(num)*14],
        "num":num,
        "nflag":1
    })

#用户管理
def umanage(request,admin,num=1):
    title = "用户管理"
    user_list = []
    db,cursor = connect()
    sql = "select * from user ORDER BY -userborth"
    cursor.execute(sql)
    i = 1
    for row in cursor.fetchall():
        user_list.append({"uid":row[0],"uname":row[1],"upwd":row[2],"uborth":row[3],"ujob":row[4],"usex":row[5]})
        i += 1
        # print row[4],"=========="
    num = int(num)
    if num == i/14:
        num = i
    else:
        num = num + 1
    close(db,cursor)
    return render_to_response("admin.html",{
        "title":title,
        "name":admin,
        "user_list":user_list[(int(num)-2) * 14:(int(num)-1)*14],
        "num":num,
        "nflag":1
    })

#删除用户
def deluser(request,admin,uid):
    db,cursor = connect()
    sql = "delete from user where userid='"+uid+"'"
    if cursor.execute(sql):
        close(db,cursor)
        return HttpResponseRedirect("/default/umanage/%s/1" % admin)

#添加用户
@csrf_exempt
def adduser(request,admin):
    if request.method == "POST":
        name = u'%s' %request.POST.get("uname")
        pwd = u'%s' %request.POST.get("upwd")
        borth = u'%s' %request.POST.get("uborth")
        job = u'%s' %request.POST.get("ujob")
        sex = u'%s' %request.POST.get("usex")
        #产生uid，以当前时间戳
        import time
        uid = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
        uone = {}
        uone["uid"]=uid;uone["uname"]=name;uone["upwd"]=pwd;uone["uborth"]=borth;uone["ujob"]=job;uone["usex"]=sex

        db,cursor = connect()
        sql = "insert into user values('"+uid+"','"+name+"','"+pwd+"','"+borth+"','"+job+"','"+sex+"')"
        cursor.execute(sql)
        close(db,cursor)

        return render_to_response("admin.html",{
            "title":"用户信息添加成功",
            "name":admin,
            "book_list":[],
            "num_list":[],
            "uflag":0,
            "usflag":1,
            "uone":uone,
        })


    return render_to_response("admin.html",{
        "title":"添加用户",
        "name":admin,
        "book_list":[],
        "num_list":[],
        "uflag":1,
    })

#管理员管理
def amanage(request,admin):
    title = "管理员管理"
    #获得管理员列表
    admin_list = []
    db,cursor = connect()
    sql = "select * from adminuser"
    cursor.execute(sql)
    for row in cursor.fetchall():
        admin_list.append({"name":row[0],"pwd":row[1]})
    return  render_to_response("admin.html",{
        "title":title,
        "name":admin,
        "admin_list":admin_list,
    })

#删除管理员
def adel(request,name,aname):
    db,cursor = connect()
    sql = "delete from adminuser where username='"+aname+"'"
    if cursor.execute(sql):
        close(db,cursor)
        return HttpResponseRedirect("/default/amanage/%s" % name)
#添加管理员
@csrf_exempt
def aadd(request,admin):
    admin_list = []
    if request.method == "POST":
        db,cursor = connect()
        name = request.POST.get("aname").encode('gbk')
        pwd = request.POST.get("apwd").encode('gbk')
        sql = "select * from adminuser WHERE username = '"+name+"'"
        if cursor.execute(sql): #如果该用户已存在
            return render_to_response("admin.html",{
                "error":"改用户已存在，请修改添加"
            })
        else:#表示该用户不存在
            sql_1 = "insert into adminuser values('"+name+"','"+pwd+"')"
            cursor.execute(sql_1)
            close(db,cursor)
            return HttpResponseRedirect("/default/amanage/%s" % admin)
    else:
        return  render_to_response("admin.html",{
        "title":"管理员管理",
        "name":admin,
        "admin_list":admin_list,
        "aflag":1,
        })

#书籍管理
def bmanage(request,admin,num=1):
    title = "书籍管理"
    book_list = []
    db,cursor = connect()
    sql = "select * from book order by -bookpdate"
    num_list =[]   #存放书的共有多少页，每页显示10个
    i = 0
    cursor.execute(sql)
    for row in cursor.fetchall():
        book_list.append({"bid":row[0],"bname":row[1],"bauthor":row[2],"btran":row[3],"bpub":row[4], \
                          "bpdata":row[5],"bscore":row[6],"bdisnum":row[7],"bshow":row[8]})
        i += 1
        if i %10 == 0 :
            num_list.append(i /10)

    num_list.append(i /10 + 1)

    return render_to_response("admin.html",{
        "title":title,
        "name":admin,
        "book_list":book_list[(int(num)-1) * 10:int(num)*10],
        "num_list":num_list,
    })

#添加书籍
@csrf_exempt
def addbook(request,admin):
    title="添加书籍信息"

    if request.method == "POST":
        db,cursor = connect()
        bid = request.POST.get("bid")
        sql_id = "select * from book where bookid='"+bid+"'"
        if cursor.execute(sql_id):
            return render_to_response("admin.html",{
                "error":"你输入的书籍id已经存在，请重新输入",
                "title":title,
                "name":admin,
                "book_list":[],
                "num_list":[],
                "bflag":1,
            })
        bid = bid.encode("utf-8")
        bname = request.POST.get("bnama").encode('utf8')
        bauthor = request.POST.get("bauthor").encode('utf8')
        btran = request.POST.get("btran").encode('utf8')
        bpub = request.POST.get("bpub").encode('utf8')
        bpdata = request.POST.get("bpdata").encode('gbk')
        if len(bpdata)==6:
            bpdata = bpdata[:4] + "0" + bpdata[4]+"0" + bpdata[5]
        elif len(bpdata)==7:
            pass
        bscore = "0.0"
        bdisnum = "0"
        bshow = request.POST.get("bshow").encode('utf8')
        sql = "insert book values('"+bid+"','"+bname+"','"+bauthor+"','"+btran+"',\
                                  '"+bpub+"','"+bpdata+"','"+bscore+"','"+bdisnum+"','"+bshow+"')"
        cursor.execute(sql)
        close(db,cursor)
        return HttpResponseRedirect("/default/show/%s/%s" % (admin,bid))

    return render_to_response("admin.html",{
        "title":title,
        "name":admin,
        "book_list":[],
        "num_list":[],
        "bflag":1,
    })


#查看书籍信息
def show(request,admin,bid):
    title = "书籍信息查看"
    one = {}
    db,cursor = connect()
    sql_1 = "select * from book where bookid='"+bid+"' "
    cursor.execute(sql_1)
    for row in cursor.fetchall():
        one["bid"] = row[0]
        one["bname"] = row[1]
        one["bauthor"] = row[2]
        one["btran"] = row[3]
        one["bpub"] = row[4]
        one["bpdata"] = row[5]
        one["bscore"] = row[6]
        one["bdisnum"] = row[7]
        one["bshow"] = row[8]
    return render_to_response("admin.html",{
            "title":title,
            "name":admin,
            "num_list":[],
            "book_list":[],
            "mflag":1,
            "one":one,
        })
    pass

#修改书籍信息
@csrf_exempt
def changebook(request,admin,bid):
    title = "书籍信息修改"

    if request.method == "POST":
        title = "书籍信息查看"
        db,cursor = connect()
        bname = request.POST.get("bnama").encode('utf8')
        bauthor = request.POST.get("bauthor").encode('utf8')
        btran = request.POST.get("btran").encode('utf8')
        bpub = request.POST.get("bpub").encode('utf8')
        # bpdata = request.POST.get("bpdata").encode('gbk')
        # #获取出版日期中的数字
        # bpdata = request.POST.get("bpdata")
        # import re
        bpdata = "20130513"
        bscore = request.POST.get("bscore").encode('utf8')
        bdisnum = request.POST.get("bdisnum").encode('utf8')
        bshow = request.POST.get("bshow").encode('utf8')
        bid = bid.encode('gbk')
        # print type(bid),bid,type(bpdata),bpdata
        sql = "update book set bookname = '"+bname+"',\
                   bookauthor='"+bauthor+"',\
                   booktrans = '"+btran+"',\
                   bookpublish = '"+bpub+"', \
                   bookpdate='"+bpdata+"',\
                   bookscore = '"+bscore+"',\
                   bookdisnum='"+bdisnum+"', \
                   bookshow='"+bshow+"' \
                   where bookid ='"+bid+"'"
        # sql = "insert book values('"+bid+"','"+bname+"','"+bauthor+"','"+btran+"',\
        #                           '"+bpub+"','"+bpdata+"','"+bscore+"','"+bdisnum+"','"+bshow+"')"
        cursor.execute(sql)
        close(db,cursor)
        return HttpResponseRedirect("/default/show/%s/%s" % (admin,bid))

    one = {}
    db,cursor = connect()
    sql = "select * from book where bookid='"+bid+"' "
    cursor.execute(sql)
    for row in cursor.fetchall():
        one["bid"] = row[0]
        one["bname"] = row[1]
        one["bauthor"] = row[2]
        one["btran"] = row[3]
        one["bpub"] = row[4]
        one["bpdata"] = row[5]
        one["bscore"] = row[6]
        one["bdisnum"] = row[7]
        one["bshow"] = row[8]

    return render_to_response("admin.html",{
        "title":title,
        "name":admin,
        "num_list":[],
        "book_list":[],
        "cflag":1,
        "one":one,
    })

#删除书籍
def bookdel(request,admin,bid):
    db,cursor = connect()
    sql = "delete from book where bookid='"+bid+"'"
    cursor.execute(sql)
    close(db,cursor)
    return HttpResponseRedirect("/default/bmanage/%s/%s" % (admin,"1"))

#书籍搜索
@csrf_exempt
def booksou(request,admin,page,num):
    if request.method=="POST":
        key = request.POST.get("key")
        choose = request.POST.get("bookcase")
        from login.views import connect,close
        db,cursor = connect()
        book_list = []
        pam = "%" + key + "%"
        if choose=="bookid":
            sql = "select * from book where bookid like %s"
        elif choose=="bookname":
            sql = "select * from book where bookname like %s"
        elif choose=="bookauthor":
            sql = "select * from book where bookauthor like %s"
        if cursor.execute(sql,pam):
            for row in cursor.fetchall():
                book_list.append({"bid":row[0],"bname":row[1],"bauthor":row[2],"bpub":row[4],"bpdata":row[5]})
        close(db,cursor)
        if book_list:  #不为空为1
            booknullflag = 0
        else: #为空
            booknullflag = 1
        if page == "1":
            num =(int(num) -1) if (int(num) -1) else 1
        else:
            num = int(num)+1
        newbook_list = book_list[(num-1) *12:(num)*12]
        if not book_list:
            booknullflag = 1
        return render_to_response("result.html",{
            "name":admin,
            "title":"搜索结果如下",
            "yes":1,
            "num":num,
            "booknullflag":booknullflag,
            "book_list":newbook_list,
            "key":key,
            "choose":choose,
        })

    return render_to_response("result.html",{
        "name":admin,
        "title":"书籍检索",
        "no":1,
        "caseflag":0,
        })
#book搜索结果处理翻页
def bookshow(request,admin,page,num,key,choose):
    from login.views import connect,close
    db,cursor = connect()
    book_list = []
    pam = "%" + key + "%"
    print key,choose,choose=="bookid"
    if choose=="bookid":
        sql = "select * from book where bookid like %s"
    elif choose=="bookname":
        sql = "select * from book where bookname like %s"
    elif choose=="bookauthor":
        sql = "select * from book where bookauthor like %s"
    if cursor.execute(sql,pam):
        for row in cursor.fetchall():
            book_list.append({"bid":row[0],"bname":row[1],"bauthor":row[2],"bpub":row[4],"bpdata":row[5]})
    close(db,cursor)
    if page == "1":
        num =(int(num) -1) if (int(num) -1) else 1
    else:
        num = int(num)+1
    newbook_list = book_list[(num-1) *12:(num)*12]
    if newbook_list:
        booknullflag2 = 0
    else: #为空
        booknullflag2 = 1
    return render_to_response("result.html",{
        "name":admin,
        "title":"搜索结果如下",
        "yes":1,
        "num":num,
        "key":key,
        "choose":choose,
        "booknullflag2":booknullflag2,
        "book_list":newbook_list,
    })

#用户搜索
@csrf_exempt
def usersou(request,admin,page=1,num=1):
    if request.method=="POST":
        key = request.POST.get("key")
        choose = request.POST.get("usercase")
        from login.views import connect,close
        db,cursor = connect()
        user_list = []
        pam = "%" + key + "%"
        if choose=="userid":
            sql = "select * from user where userid like %s"
        elif choose=="username":
            sql = "select * from user where username like %s"
        elif choose=="userborth":
            sql = "select * from user where userborth like %s"
        elif choose=="userjob":
            sql = "select * from user where userjob like %s"
        if cursor.execute(sql,pam):
            for row in cursor.fetchall():
                user_list.append({"uid":row[0],"uname":row[1],"uborth":row[3],"ujob":row[4],"usex":row[5]})
        close(db,cursor)
        if user_list:  #不为空为1
            nullflag = 0
        else: #为空
            nullflag = 1
        if page == "1":
            num =(int(num) -1) if (int(num) -1) else 1
        else:
            num = int(num)+1
        newuser_list = user_list[(num-1) *14:(num)*14]
        if not newuser_list:
            nullflag = 1
        return render_to_response("result.html",{
            "name":admin,
            "title":"搜索结果如下",
            "yes":1,
            "num":num,
            "key":key,
            "choose":choose,
            "nullflag":nullflag,
            "user_list":newuser_list,
        })

    return render_to_response("result.html",{
        "name":admin,
        "title":"用户检索",
        "no":1,
        "num":num,
        "caseflag":1,
        })
#用户搜索结果翻页实现
def usershow(request,admin,page,num,key,choose):
    from login.views import connect,close
    db,cursor = connect()
    user_list = []
    pam = "%" + key + "%"
    if choose=="userid":
        sql = "select * from user where userid like %s"
    elif choose=="username":
        sql = "select * from user where username like %s"
    elif choose=="userborth":
        sql = "select * from user where userborth like %s"
    elif choose=="userjob":
        sql = "select * from user where userjob like %s"
    if cursor.execute(sql,pam):
        for row in cursor.fetchall():
            user_list.append({"uid":row[0],"uname":row[1],"uborth":row[3],"ujob":row[4],"usex":row[5]})
    close(db,cursor)
    if user_list:  #不为空为1
        nullflag2 = 0
    else: #为空
        nullflag2 = 1
    if page == "1":
        num =(int(num) -1) if (int(num) -1) else 1
    else:
        num = int(num)+1
    newuser_list = user_list[(num-1) *14:(num)*14]
    if not newuser_list:
        nullflag2 = 1
    return render_to_response("result.html",{
        "name":admin,
        "title":"搜索结果如下",
        "yes":1,
        "num":num,
        "key":key,
        "choose":choose,
        "nullflag2":nullflag2,
        "user_list":newuser_list,
    })