#-*-coding:utf-8-*-
class GlobalUse(object):

    def __init__(self):
        self.bookid_list = []   #存放登录用户的推荐书本信息
        self.userid_list = []   #存放登陆用户的相似用户信息
        self.seeBook_list = []   #存放登陆用户的相似用户信息

    #设置登录用户的书本推荐
    def setBookId(self,brid_list):
        self.bookid_list = brid_list

    #设置登录用户的user推荐
    def setUserId(self,urid_list):
        self.userid_list=urid_list

    #设置登录用户的看过的书
    def setSeeBook(self,seeBook_list):
        self.seeBook_list=seeBook_list