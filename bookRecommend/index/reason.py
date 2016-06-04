#-*-coding:utf-8-*-
from login.views import connect,close
from basedUserCF import *
from login.views import userrecommend

def getReason():
    bid_list= userrecommend.bookid_list     #为你推荐的书的id列表
    near_list = userrecommend.userid_list[:3] #根据这三个人来推荐书的，推荐算法中是一致的
    # print near_list
    reason = []               #用来保存需要显示推荐理由的一些信息
    #对推荐的所有书进行遍历，得到推荐人与当前用户的相似度，他给这本书的打分，以及该用户的姓名
    for bid in bid_list:
        # print "bid:",bid
        db,cursor = connect()
        sql = "select userid,score from uid_to_bid where bookid = '"+bid+"'"
        cursor.execute(sql)
        for row in cursor.fetchall():
            #对推荐的三个人进行遍历，决定当前书是来自哪个人的评分
            for near in near_list:
                if row[0]==near[0]:
                    uid = row[0]
                    # print "uid:",uid
                    bscore = row[1]
                    # print "score",score
                    sim = near[1]
                    # print "sim",sim

                    sql_1 = "select username from user where userid = '"+uid+"'"
                    cursor.execute(sql_1)
                    for row_1 in cursor.fetchall():
                        uname = row_1[0]
                    # print uname1
                    reason.append({"name":uname, "id":bid, "score":bscore, "simv":sim})
                    break
                break

    return reason