#-*- coding: UTF-8 -*-
import urllib
import urllib2
import re
import urlparse
import threading
import time
import MySQLdb
from time import ctime, sleep
import requests
import os
import csv
csvfile = file('9.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['书籍链接', '书名', '评分', '评论人数'])


start_url = 'https://book.douban.com/tag/小说?start=1000&type=T'#所有热门标签页面
headers = {'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/4.0)'}
urls = []
types = []
urls1 = []
urls2 = []
book_url = []
next_url = []
new_url = []
book_url = []
book_name = []
book_score = []
#book_comment = []


#request = urllib2.Request(start_url,headers=headers)
#response = urllib2.urlopen(request)
#content = response.read()
#pattern = re.compile('\s<td><a\shref=\"(.*?)\"\sclass="tag">(.*?)</a></td>',re.S)
#items = re.findall(pattern, content)
#for item in items:
    #url2 = urlparse.urljoin(start_url,item[0])
    #urls.append(url2)#将超链接存入urls[]
    #types.append(item[1])#书籍类型
#print urls
#print types



request1 = urllib2.Request(start_url, headers=headers)
response1 = urllib2.urlopen(request1)
content1 = response1.read()
#print urls[i]
#print content1
#pattern1 = re.compile('<span\sclass="next">\s+<link.*?>\s+<a\shref="(.*?)"\s>.*?</a>',re.S)
#items1 = re.findall(pattern1, content1)
    #print items1


    #print urls1[0]

#next_url = urlparse.urljoin(start_url,items1[0])#下一页的链接
#urls2.append(next_url)
    #print urls2

pattern1_book = re.compile('<h2\sclass="">\s+<a href="(.*?)"\stitle="(.*?)".*?>.*?<span class="allstar(.*?)">.*?<span class="pl">.*?\((.*?)\)',re.S)
items1_book = re.findall(pattern1_book, content1)
for line in items1_book:
        writer.writerow(line)
#for j in range(len(items1_book)):
#book_url.append(items1_book[j][0])#书的内容的链接
    #print book_url
    #print len(items1_book)
csvfile.close()
