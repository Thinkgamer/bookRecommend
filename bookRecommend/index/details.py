#-*-coding:utf8-*-

def getOneBook(bid,flag):
    from login.views import connect, close
    db,cursor = connect()
    sql_d = "select * from book where bookid="+bid+""
    sql_b = "select * from bookbuy where bookid="+bid+""
    cursor.execute(sql_d)
    if len(cursor.fetchall()):
        cursor.execute(sql_d)
        onebook={}  #存放book的相关信息
        onebookbuy = [] #存放购买的详细信息
        print "book"
        for row in cursor.fetchall():
            onebook["bid"] = row[0]
            onebook["bname"] = row[1]
            onebook["bauthor"] = row[2]
            onebook["btrans"] = row[3]
            onebook["bpublish"] = row[4]
            onebook["bpdate"] = row[5]
            onebook["bscore"] = row[6]
            onebook["bdisnum"] = row[7]
            onebook["bshow"] = row[8]

        cursor.execute(sql_b)
        for row_b in cursor.fetchall():
            onebookbuy.append({"store":row_b[2],"price":row_b[3],"bhref":row_b[1]})
        return onebook,onebookbuy
    else:
        print "newbook"
        onebook={}  #存放book的相关信息
        onebookbuy = [] #存放购买的详细信息
        sql_d2 = "select * from newbook where bookid="+bid+""
        sql_b2 = "select * from newbookbuy where bookid="+bid+""

        cursor.execute(sql_d2)
        for row in cursor.fetchall():
            onebook["bid"] = row[0]
            onebook["bname"] = row[1]
            onebook["bauthor"] = row[2]
            onebook["btrans"] = row[3]
            onebook["bpublish"] = row[4]
            onebook["bpdate"] = row[5]
            onebook["bscore"] = row[6]
            onebook["bdisnum"] = row[7]
            onebook["bshow"] = row[8]
        cursor.execute(sql_b2)
        for row_b in cursor.fetchall():
            onebookbuy.append({"store":row_b[2],"price":row_b[3],"bhref":row_b[1]})
        print onebook,onebookbuy
        return onebook,onebookbuy

def getSimUser(uid_list):
    from login.views import connect, close
    uname_list=[]
    db,cursor = connect()
    for uid in uid_list:
        simValue = float(uid[1]) * 100
        sql = "select username from user where userid='"+uid[0]+"'"
        cursor.execute(sql)
        for row in cursor.fetchall():
            uname_list.append({"username":row[0],"usersim":str("%.1f" % simValue)})
    close(db,cursor)
    return uname_list

def getOtherBook(bid):
    from login.views import connect, close
    otherbook_list = []
    db,cursor = connect()

    sql = "select bookid,bookname from book order by rand() limit 5"
    cursor.execute(sql)
    for row in cursor.fetchall():
        if row[0]!=bid:
            otherbook_list.append({"bid":row[0],"bname":row[1]})
    return otherbook_list

def getseeBook(uid):
    from login.views import connect, close
    book_list = []
    db,cursor = connect()
    sql = "select bookid from uid_to_bid where userid='"+uid+"' "
    cursor.execute(sql)
    for row in cursor.fetchall():
        bid = row[0]
        sql_1 = "select bookid,bookname,bookshow from book where bookid = '"+bid+"'"
        cursor.execute(sql_1)
        for row_1 in cursor.fetchall():
            book_list.append({"bid":row_1[0],"bname":row_1[1],"bshow":row_1[2]})

    close(db,cursor)
    return book_list