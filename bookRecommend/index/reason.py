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
        uname=""
        bscore=0.0
        sim = 0.0
        snum = 0
        simnum = 0
        for near in near_list:
            db,cursor = connect()
            sql = "select userid,score from uid_to_bid where userid = '"+near[0]+"' and bookid='"+bid+"'"
            if cursor.execute(sql): #如果存在
                for row in cursor.fetchall():
                    bscore += float(row[1])
                sql_1 = "select username from user where userid = '"+near[0]+"'"
                cursor.execute(sql_1)
                for row_1 in cursor.fetchall():
                    uname += " \" %s\" " % row_1[0] + ","
                sim += float(near[1])
                snum += 1
                simnum += 1
        # print uname,"--",bscore/3,"--",sim/3
        reason.append({"name":uname[:-1], "id":bid, "score":bscore / snum, "simv":sim /simnum})
    return reason
        # sql = "select userid,score from uid_to_bid where bookid = '"+bid+"'"
        # cursor.execute(sql)
        # uname = ""
        # bscore =0.0
        # sim = 0.0
        # for row in cursor.fetchall():
        #     #对推荐的三个人进行遍历，决定当前书是来自哪个人的评分
        #     if row[0] in near_list:
        #         for near in near_list:
        #             uid = row[0]
        #             # print "uid:",uid
        #             bscore += float(row[1])
        #             # print "score",score
        #             sim += near[1]
        #             # print "sim",sim
        #
        #             sql_1 = "select username from user where userid = '"+uid+"'"
        #             cursor.execute(sql_1)
        #             for row_1 in cursor.fetchall():
        #                 uname += row_1[0] + ","
        #             # print uname1
        #         print uname,"--",bscore,"--",sim
        #         reason.append({"name":uname[:-1], "id":bid, "score":bscore /3, "simv":sim /3})

    # return reason