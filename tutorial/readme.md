近半个月的编码，第一只像样的爬虫终于出炉了，简单介绍一下这只爬虫的设计实现和功能  
该爬虫实现对拉勾网上python相关职位信息的爬取，学习采用了一些技术，以下做简单介绍  
环境：Python 3.6   Scrapy 1.4.0  Mysql 5.7  
需要安装的库  
pip install fake_useragent      
pip install pymysql  
刚刚接触爬虫就用上了Scrapy爬虫框架，requests加beautifulsoup组合在lagou.py和lagou_login.py中使用  
* item.py中定义了四个item,包括position(职位), money(薪酬), industry(行业), href(该岗位具体信息的超链接)  
* middlewares.py中使用了随机动态变换User-Agent的RandomUserAgentMiddleware类，在settings.py中配置使用，但是对拉勾网并没有什么作用，看来只能加入对ip地址的变换才能突破拉勾网的限制
* pipelines.py中实现了向json文件和Mysql数据库的写入(据说Scrapy和Mongodb更搭配，使用起来更方便，以后加入对Mongodb的写入)
对Mysql的写入需要在settings.py中配置自己数据库的相关信息并且创建一张空白表使得Scrapy可以向其中写入数据
* settings.py中配置了Scrapy的相关信息......
* lagou_spider.py是爬虫的主体：在爬虫过程中实现了对拉勾网的模拟登录(过程很纠结，先是对密码进行了双重md5加密算法，还有将动态token写入headers,使用FormRequet()方法提交表单，完成登录，回调函数的使用还有yield的使用值得学习),使用Xpath对html页面进行解析，动态token的提取使用了正则表达式提取相关value，提取出item的相关信息后按settings配置输出
