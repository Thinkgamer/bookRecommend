#-*-coding:utf-8-*-

'''''
Created on 2016-5-30

@author: thinkgamer
'''
import math
import MySQLdb
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

class ItemBasedCF:
    def __init__(self):
        self.readData()

    def readData(self):
        #读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()     #用户-物品的评分表
        db,cursor = connect()
        sql = "select * from uid_to_bid"
        cursor.execute(sql)
        for row in cursor.fetchall():
            if row[0].encode("gbk") not in self.train:
                self.train[row[0].encode("gbk")] = {}
            self.train[row[0].encode("gbk")][row[2]]=float(row[1])

        close(db,cursor)

    def ItemSimilarity(self):
        #建立物品-物品的共现矩阵
        C = dict()  #物品-物品的共现矩阵
        N = dict()  #物品被多少个不同用户购买
        for user,items in self.train.items():
            for i in items.keys():
                N.setdefault(i,0)
                N[i] += 1
                C.setdefault(i,{})
                for j in items.keys():
                    if i == j : continue
                    C[i].setdefault(j,0)
                    C[i][j] += 1
        #计算相似度矩阵
        self.W = dict()
        for i,related_items in C.items():
            self.W.setdefault(i,{})
            for j,cij in related_items.items():
                self.W[i][j] = cij / (math.sqrt(N[i] * N[j]))
        return self.W

    #给用户user推荐，前K个相关用户
    def Recommend(self,user,K=3,N=5):
        rank = dict()
        action_item = self.train[user]     #用户user产生过行为的item和评分
        for item,score in action_item.items():
            for j,wj in sorted(self.W[item].items(),key=lambda x:x[1],reverse=True)[0:K]:
                if j in action_item.keys():
                    continue
                rank.setdefault(j,0)
                rank[j] += score * wj
        return dict(sorted(rank.items(),key=lambda x:x[1],reverse=True)[0:N])

def recommend(uid):
    bookid_list = []
    #声明一个ItemBased推荐的对象
    Item = ItemBasedCF()
    Item.ItemSimilarity()
    recommedDic = Item.Recommend(uid)
    for k,v in recommedDic.iteritems():
        db,cursor = connect()
        sql = "select bookname from book where bookid = '"+k+"'"
        n = cursor.execute(sql)
        if n ==1:
            for row in cursor.fetchall():
                bname = row[0]
            bookid_list.append({"bsim":v,"bname":bname,"bid":k})
        else:
            sql_1 = "select bookname from newbook where bookid = '"+k+"'"
            cursor.execute(sql_1)
            for row_1 in cursor.fetchall():
                bname = row_1[0]
            bookid_list.append({"bsim":v,"bname":bname,"bid":k})
        # print k,"=======",v
    return bookid_list
