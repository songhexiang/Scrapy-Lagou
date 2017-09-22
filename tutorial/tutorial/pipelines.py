# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
from scrapy import log
from tutorial import settings
from tutorial.items import *

#写入数据库管道
class TutorialPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            for i in range(len(item['position'])):
                self.cursor.execute('insert into lagouinfo values (%s, %s, %s, %s)', (item['position'][i], item['money'][i], item['industry'][i], item['href'][i]))
            self.connect.commit()
        except Exception as error:
            log(error)
        return item

#写入json文件        
class jsonPipeline(object):
    def __init__(self):
        self.filename = open("lagou.json", "wb")
    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item), ensure_ascii=False)+",\n"
        self.filename.write(jsontext.encode("utf-8"))
        return item
    def close_spider(self, spider):
        self.filename.close()