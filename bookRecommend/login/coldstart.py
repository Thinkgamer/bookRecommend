#-*-coding:utf-8-*-
from views import connect,close

def coldstart(uid):
    #获取该用户的出生年份，工作和性别
    db,cursor = connect()
    sql_u = "select userborth,userjob,usersex from user where userid = '"+uid+"'"
    cursor.execute(sql_u)
    for row in cursor.fetchall():
        borth = row[0].encode("utf-8")
        job = row[1].encode("utf-8")
        sex = row[2].encode("utf-8")
    borth1 = str(borth)
    borth2 = str(borth)
    # print "borth1:",borth1,"borth2:",borth2
    #从数据库中查询与该用户特征值相似的用户
    bid_list = []
    uid_list = []
    k = 0
    i = 0
    while k < 3 and i<12: #k < 3是年龄上下3 ,i<12是推荐的book小于12
        # print sex,job,borth1,borth2,k,i
        sql_all = "select userid from user where usersex = '"+sex+"' and userjob = '"+job+"'and userborth <='"+borth1+"' and userborth>='"+borth2+"'"
        if cursor.execute(sql_all): #如果查询不为空
            for row_all in cursor.fetchall():
                # print "ssimuid:",row_all[0]
                simuid = row_all[0] #相似用户id
                if simuid != uid and simuid not in uid_list: #保证user id不重复
                    uid_list.append((simuid,0.8))
                    # print "ssimuid:",simuid
                    #从uid_to_bid表中获取相似用户看过的书的id
                    sql_bid = "select bookid from uid_to_bid where userid='"+simuid+"'"
                    if cursor.execute(sql_bid):
                        for row_bid in cursor.fetchall():
                            if i <12 and row_bid[0] not in bid_list: #保证book id不重复
                                bid_list.append(row_bid[0])
                                i += 1
                            if i>=12:
                                break
                if i>=12:
                    break
        k += 1
        borth1 = str(int(borth1)+1) #year的上下限各加1进行查找
        borth2 = str(int(borth2)-1)
        # print "sss"


    #如果为其推荐的书本少于12本，选择相同职业的其他用户看过的书
    if len(bid_list)<12:                    #将其书本书增加为12本
        # print "not engout"
        len_bid = 12-len(bid_list)
        sql_job = "select userid from user where userjob = '"+job+"' and usersex='"+sex+"'"
        if cursor.execute(sql_job):
            for row_job in cursor.fetchall():
                if row_job[0] not in uid_list and row_job[0] != uid: #保证user id不重复且不等于uid
                    uid_list.append((row_job[0],0.8))
                    #从uid_to_bid中获取相似用户看过的书的id
                    sql_bid_2 = "select bookid from uid_to_bid where userid='"+row_job[0]+"'"
                    if cursor.execute(sql_bid_2):
                            for row_bid_2 in cursor.fetchall():
                                if row_bid_2[0] not in bid_list:   #保证book id不重复
                                    if len_bid:
                                        bid_list.append(row_bid_2[0])
                                        len_bid-=1
                                    else:
                                        break
                    if not len_bid:
                        break

    #如果为其推荐的书本少于12本，选择相同不同职业的其他用户看过的书
    if len(bid_list)<12:                    #将其书本书增加为12本
        print "not engout"
        len_bid = 12-len(bid_list)
        sql_sex_age = "select userid from user where usersex='"+sex+"' and userborth <='"+str(int(borth)+10)+"' and userborth >='"+str(int(borth)-10)+"'"
        if cursor.execute(sql_sex_age):
            for row_sex in cursor.fetchall():
                if row_sex[0] not in uid_list and row_sex[0] != uid: #保证user id不重复且不等于uid
                    uid_list.append((row_sex[0],0.8))
                    #从uid_to_bid中获取相似用户看过的书的id
                    sql_bid_3 = "select bookid from uid_to_bid where userid='"+row_sex[0]+"'"
                    if cursor.execute(sql_bid_3):
                            for sql_bid_3 in cursor.fetchall():
                                if sql_bid_3[0] not in bid_list:   #保证book id不重复
                                    if len_bid:
                                        bid_list.append(sql_bid_3[0])
                                        len_bid-=1
                                    else:
                                        break
                    if not len_bid:
                        break

    # #获取这12本书的信息
    # book_list = []
    # for bid in bid_list:
    #     sql_mess = "select * from book where bookid = '"+bid+"'"
    #     if cursor.execute(sql_mess):
    #         for row_mess in cursor.fetchall():
    #             book_list.append({"bid":row_mess[0],"bname":row_mess[1],"bauthor":row_mess[2],"btran":row_mess[3], \
    #                               "bpublish":row_mess[4],"bpdata":row_mess[5],"bscore":row_mess[6],"bdisnum":row_mess[7]})


    close(db,cursor)
    return bid_list,uid_list[:10]

def getItemBook(bid_list):
    from login.views import connect,close
    bookid_list = []
    db,cursor = connect()
    for bid in bid_list:
        sql = "select bookname from book where bookid='"+bid+"'"
        cursor.execute(sql)
        for row in cursor.fetchall():
            bname = row[0]

        bookid_list.append({"bsim":0.8,"bname":bname,"bid":bid})
    close(db,cursor)
    return  bookid_list
