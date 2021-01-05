# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from scrapy import signals
from twisted.enterprise import adbapi 
from pymysql import cursors


# # 去重
# class DuplicatesPipeline(object):

#     def __init__(self, dbpool):

#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(
#             host=settings[ "MYSQL_HOST" ],
#             db=settings[ "MYSQL_DBNAME" ],
#             user=settings[ "MYSQL_USER" ],
#             passwd=settings[ "MYSQL_PASSWORD" ],
#             port=settings["MYSQL_PORT"],
#             charset='utf8' ,
#             cursorclass=cursors.DictCursor,
#             use_unicode=True,
#         )
#         dbpool = adbapi.ConnectionPool("pymysql" , **dbparms)
 
#         return  cls(dbpool) 


#     def process_item(self, item, spider):
#         if Redis.exists('url:%s' % item['url']):
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             Redis.set('url:%s' % item['url'],1)
#             return item




class  MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
        self._sql = ''
        #去重item
        self.set_sku = set() 
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings[ "MYSQL_HOST" ],
            db=settings[ "MYSQL_DBNAME" ],
            user=settings[ "MYSQL_USER" ],
            passwd=settings[ "MYSQL_PASSWORD" ],
            port=settings["MYSQL_PORT"],
            charset='utf8' ,
            cursorclass=cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("pymysql" , **dbparms)
 
        return  cls(dbpool)
    #addCallback函数返回，result是查询结果，item是要存入的数据
    #如果表内已经有数据，则直接返回，不再保存数据。
    def filter_item(self, result, item, spider):
        if result:
            return item
        else:

            query = self.dbpool.runInteraction(self.do_insert, item)
            query.addErrback(self.handle_error, item, spider) #处理异常
            # query = self.dbpool.runInteraction(self.do_insert_b2, item)
            # query.addErrback(self.handle_error, item, spider) #处理异常
 
    def process_item(self, item, spider):

        query = self.dbpool.runQuery("SELECT good_sku from good_sku_copy where good_sku=%s", item["good_sku"])
        query.addCallback(self.filter_item, item, spider)
        query.addErrback(self.handle_error, item, spider) #处理异常        

        return item


    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)

    def do_insert(self, cursor, item):
        cursor.execute("insert into good_sku_copy(id, good_sku) values(null, %s)", item["good_sku"])
        cursor.execute(self.sql, 
                        (item["website"],
                        item["brand"], 
                        item["shop_name"], 
                        item["shop_url"], 
                        item["good_sku"], 
                        item["good_title"], 
                        item["good_price"], 
                        item["good_detail"], 
                        item["good_color"],     
                        item["good_tips"]))

    @property
    def sql(self):
        if not self._sql:
            self._sql = ''' 
            insert  into yurongfu_n_copy(id, website, brand, shop_name, shop_url, good_sku, good_title, good_price, good_detail, good_color, good_tips) 
               values(null, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            return self._sql
        return self._sql

    def close_spider(self, spider):
        print("爬取完成，关闭数据库")
        self.dbpool.close()