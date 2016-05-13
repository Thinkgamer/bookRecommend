#-*- coding: UTF-8 -*-
import urllib
import urllib2
import re
import urlparse
import threading
import time
from time import ctime, sleep
import requests
import os

import csv
csvfile = file('douban_users0.csv', 'wb')
writer = csv.writer(csvfile)
writer.writerow(['用户ID', '评分', '书名'])

start_url = 'https://book.douban.com/tag/小说?start=60&type=T'
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
book_comment = []
k = 1

request = urllib2.Request(start_url,headers=headers)
response = urllib2.urlopen(request)
content = response.read()
pattern = re.compile('<h2\sclass="">\s+<a\shref="(.*?)"')
items = re.findall(pattern, content)
for item in items:
    print item
    book_url.append(item)
for i in range(len(book_url)):

    request1 = urllib2.Request(book_url[i],headers=headers)
    response1 = urllib2.urlopen(request1)
    content1 = response1.read()
    pattern1 = re.compile('<span\sclass="pl">\(<a\shref="(.*?)">.*?</span>条</a>',re.S)
    items1 = re.findall(pattern1, content1)
    if len(items1) > 0:
        print items1[0]
        while k == 1:
            request2 = urllib2.Request(items1[0],headers=headers)
            response2 = urllib2.urlopen(request2)
            content2 = response2.read()
            pattern2 = re.compile('<span\sclass="starb">.*?<a\shref=".*?/people/(.*?)/"\sclass.*?>(.*?)</a>.*?<span\sclass="allstar(.*?)".*?>',re.S)
            items2 = re.findall(pattern2, content2)
            for item2 in items2:
                writer.writerow(item2)
                print item2[0],item2[1],item2[2]
            pattern2_next = re.compile('<span\sclass="next">.*?<a\shref="(.*?)"\s>',re.S)
            items2_next = re.findall(pattern2_next, content2)
            #print items2_next[0]
            if len(items2_next) > 0:
                items1[0] = items2_next[0]
            else:
                break
            continue
    else:
        continue




csvfile.close()
#print book_url
#print len(book_url)