#-*-coding:utf-8-*-
from login.views import connect,close

def getOneAuthor(bid):
    bmess_list = []
    db,cursor = connect()
    author = ""
    #获取该书的作者
    sql_1 = "select bookauthor from book where bookid = '"+bid+"'"
    cursor.execute(sql_1)
    for row_1 in cursor.fetchall():
        author = row_1[0]
    #书单中不存在，往新书中找
    if not author:
        sql_11 = "select bookauthor from book where bookid = '"+bid+"'"
        cursor.execute(sql_11)
        for row_11 in cursor.fetchall():
            author = row_11[0]

    #获取该作者的其他书籍
    sql_2 = "select bookid,bookname from book where bookauthor = '"+author+"' and bookid != '"+bid+"'"
    cursor.execute(sql_2)
    for row_2 in cursor.fetchall():
        # print row_2[0]
        bmess_list.append({"bid":row_2[0],"bname":row_2[1]})

    #在新书中查找
    sql_22 = "select bookid,bookname from newbook where bookauthor = '"+author+"' and bookid != '"+bid+"'"
    cursor.execute(sql_22)
    for row_22 in cursor.fetchall():
        for i in range(len(bmess_list)):
            if row_22[0] == bmess_list[i]["bid"]:
                continue
        print row_22[0]
        bmess_list.append({"bid":row_22[0],"bname":row_22[1]})

    close(db,cursor)
    return bmess_list

#获取用户对book的评分
def getScore(uid,bid):
    db,cursor = connect()
    sql = "select score from uid_to_bid where userid='"+uid+"' and bookid='"+bid+"'"
    n = cursor.execute(sql)
    if n ==1:
        for row in cursor.fetchall():
            score = row[0]
    else:
        score = 0
    close(db,cursor)
    return score

#将评分写入数据库
def writeScore(uid,score,bid):
    db,cursor = connect()
    if getScore(uid,bid):
        sql = "update uid_to_bid set score = '"+str(score)+"' where userid='"+uid+"' and bookid = '"+bid+"'"
    else:
        sql = "insert into uid_to_bid values('"+uid+"','"+str(score)+"','"+bid+"')"
    cursor.execute(sql)
    close(db,cursor)
