# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import logging


class MySQLPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='192.168.2.200', port=3306, user='windows', password='123456', db='spider', charset='utf8')
        self.cursor = self.conn.cursor()
        sql = """
              CREATE TABLE IF NOT EXISTS jingdong(
              title VARCHAR(100) NOT NULL,
              shop VARCHAR(30) NOT NULL,
              price VARCHAR(10) NOT NULL,
              comment VARCHAR(10) NOT NULL,
              keyword VARCHAR(10) NOT NULL,
              page VARCHAR(3) NOT NULL,
              time VARCHAR(20) NOT NULL,
              PRIMARY KEY (title, shop)
              );
              """
        self.cursor.execute(sql)
        self.logger = logging.getLogger(__name__)

    def __del__(self):
        self.conn.close()

    def process_item(self, item, spider):
        sql = 'REPLACE INTO jingdong (title, shop, price, comment, keyword, page, time) ' \
              'VALUES (%s, %s, %s, %s, %s, %s, %s)'
        try:
            self.cursor.execute(sql, (item.get('title'), item.get('shop'), item.get('price'), item.get('comment'),
                                      item.get('keyword'), item.get('page'), item.get('time')))
            self.conn.commit()
        except Exception as e:
            self.logger.error('{0}:{1}'.format(type(e), e.args))
            self.conn.rollback()
        return item
