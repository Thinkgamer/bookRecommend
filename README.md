BookRecommend
图书推荐系统，依托豆瓣的图书和评分信息，使用基于items的推荐算法，实现推荐<br><br>

1：环境说明<br>
Mysql 5.6 + python 2.7 + django 1.8 + MySQLdb<br><br>

2：文件夹说明<br>
bookrecommend：是项目综合展示的目录，是一个django的工程，使用时，只需在该目录下打开cmd，运行manage.py runserver 即可<br><br>


数据集：里边是项目所需要的数据集<br>
        books.csv:书本的相关信息<br>
	users.csv:用户的相关信息<br>
	uid_score_bid.csv:用户给书本的打分信息<br><br>
数据库备份：使用时在数据中新建一个bookrecommend数据库，导入sql文件即可<br><br>

算法原型：协同过滤基于items的推荐算法<br><br>

3：爬取数据部分代码暂时不提供，有需要的话联系邮箱：thinkgamer@163.com
