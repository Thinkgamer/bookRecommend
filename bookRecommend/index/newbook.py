#-*-coding:utf-8-*-
from index.basedUserCF import *

def getNewBook():
    from login.views import connect,close
    newBook = []
    db,cursor = connect()
    sql = "select * from newbook"
    cursor.execute(sql)
    for row in cursor.fetchall():
        newBook.append({"bid":row[0],"bname":row[1],"btime":row[5],"bshow":row[-1]})
    close(db,cursor)
    return newBook

def getHotBook():
    from login.views import connect,close
    hotBook = []
    db,cursor = connect()
    sql = "select * from book ORDER BY -bookdisnum"
    cursor.execute(sql)
    for row in cursor.fetchall():
        hotBook.append({"bid":row[0],"bname":row[1],"bdisnum":row[-2],"bshow":row[-1]})
    close(db,cursor)
    return hotBook

def getYouLoveBook(bookid_list):
    from index.reason import *
    reason_list = getReason()

    from login.views import connect,close
    bookLove_list = []
    db,cursor = connect()
    for bid in bookid_list:
        sql = "select * from book where bookid = '"+bid+"'"
        cursor.execute(sql)
        for row in cursor.fetchall():
            for reason in reason_list:
                if row[0]==reason.get("id"):
                    bookLove_list.append({"bid":row[0],"bname":row[1],"bshow":row[-1],"bdisnum":1,"btime":1,"uname":reason.get("name"),"sim":reason.get("simv"),"score":reason.get("score")})

    close(db,cursor)
    return bookLove_list