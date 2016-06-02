#-*- coding:utf-8-*-
from django.shortcuts import render_to_response
import details as get
from newbook import getNewBook,getHotBook,getYouLoveBook
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def getName(uid):
    from login.views import connect,close
    db,cursor = connect()
    sql = "select username from user where userid='"+uid+"' "
    cursor.execute(sql)
    for row in cursor.fetchall():
        close(db,cursor)
        return row[0]

#猜你喜欢模块
def index(request,uid):
    from login.views import userrecommend
    #获得新书列表
    newBook_list =getNewBook()[:8]

    #获得hot图书列表
    hotBook_list =getHotBook()[:4]

    #获得相似用户列表
    uid_list=userrecommend.userid_list
    usersim_list = get.getSimUser(uid_list)
    username = getName(uid)

    #获得为你推荐的书籍
    loveLook_list = getYouLoveBook(userrecommend.bookid_list)


    return  render_to_response("index.html",{
        "username":username,
        "uid":uid,
        "usersim_list":usersim_list,
        "newBook_list":newBook_list[::-1],
        "hotBook_list":hotBook_list[::-1],
        "loveLook_list":loveLook_list[:3],
    })

def more(request,uid):
    from login.views import userrecommend
    #获得相似用户列表
    uid_list=userrecommend.userid_list
    usersim_list = get.getSimUser(uid_list)

    username = getName(uid)

    #获得为你推荐的书籍
    loveLook_list = getYouLoveBook(userrecommend.bookid_list)

    return  render_to_response("more.html",{
        "username":username,
        "uid":uid,
        "usersim_list":usersim_list,
        "title":"猜你喜欢",
        "book_list":loveLook_list,
    })

@csrf_exempt
def details(request,uid,bid):
    #获得一本书的具体信息和购买信息
    onebook,onebookbuy = get.getOneBook(bid,"newbook")
    username = getName(uid)
    #获取评论过该本书的还评论过那些书
    otherbook_list = get.getOtherBook(bid)
    #判断当前用户是否对该本书打过分
    import other
    score = other.getScore(uid,bid)

    #基于Item的推荐
    from login.views import userrecommend
    itembook_list = userrecommend.itembook_list

    #如果是提交分数
    if request.method=="POST":
        score = request.POST.get("score")
        try:
            score = float(score) if float(score)<5.0 else 3.0
        except:
            return  render_to_response("details.html",{
                "username":username,
                "uid":uid,
                "onebook":onebook,
                "onebookbuy":onebookbuy,
                "otherbook_list":otherbook_list[:4],
                "error":"你输入的数据不合法，请重新输入",
                "flag":1,
                "book_list":sorted(itembook_list,reverse=True),
             })
        finally:
            # print score
            pass
        if not username:        #还没有登录
             # print score
             return  render_to_response("details.html",{
                 "username":username,
                 "uid":uid,
                 "onebook":onebook,
                 "onebookbuy":onebookbuy,
                 "otherbook_list":otherbook_list[:4],
                 # "bmess_list":bmess_list[:4],
                 "error":"你还没有登陆，是否登录？",
                 "flag":0,
                 "book_list":sorted(itembook_list,reverse=True),
             })
        other.writeScore(uid,score,bid)     #将打分写入数据库
        return render_to_response("details.html",{
            "username":username,
            "uid":uid,
            "onebook":onebook,
            "onebookbuy":onebookbuy,
            "otherbook_list":otherbook_list[:5],
            # "bmess_list":bmess_list[:4],
            "score":score,
            "book_list":sorted(itembook_list,reverse=True),
        })

    return  render_to_response("details.html",{
        "username":username,
        "uid":uid,
        "onebook":onebook,
        "onebookbuy":onebookbuy,
        "otherbook_list":otherbook_list[:4],
         # "bmess_list":bmess_list[:4],
        "score":score,
        "book_list":sorted(itembook_list,reverse=True),
    })


def new(request,uid):
    from login.views import userrecommend
    #获得新书列表
    newBook_list =getNewBook()

    #获得相似用户列表
    uid_list=userrecommend.userid_list
    usersim_list = get.getSimUser(uid_list)
    username = getName(uid)
    return  render_to_response("more.html",{
        "username":username,
        "uid":uid,
        "usersim_list":usersim_list,
        "title":"新书速递",
        "book_list":sorted(newBook_list,key=lambda book:book.get("btime"),reverse=True)[:20],
    })

def hot(request,uid):
    from login.views import userrecommend
    #获得hot book列表
    hotBook_list =getHotBook()

    #获得相似用户列表
    uid_list=userrecommend.userid_list
    usersim_list = get.getSimUser(uid_list)
    username = getName(uid)
    return  render_to_response("more.html",{
        "username":username,
        "uid":uid,
        "usersim_list":usersim_list,
        "title":"Hot 榜",
        "book_list":hotBook_list[:20],
    })
