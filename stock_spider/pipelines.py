# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql

from stock_spider.items import StockDividendItem
from stock_spider.items import StockIndexItem
from stock_spider.items import StockInfoItem
from stock_spider.items import StockMarketItem
from stock_spider.items import StockShareHolderItem

# 使用debug环境
DEBUG = True
if DEBUG:
    db_name = "stock_spider"
    db_user = "root"
    db_password = "123456"
    db_host = "localhost"
    db_port = 3306
else:
    db_name = "stock_spider"
    db_user = "root"
    db_password = "123456"
    db_host = "localhost"
    db_port = 3306

# 将抓取到的股票行情数据信息保存进Mysql数据库
class StockSpiderPipeline(object):
    def __init__(self):
        # 初始化打开数据库连接
        self.conn = pymysql.Connect(
            host=db_host,
            port=db_port,
            user=db_user,
            db=db_name,
            passwd=db_password,
            charset='utf8'
        )
        # 使用cursor()方法创建一个游标对象cursor
        self.cursor = self.conn.cursor()

        # 清空表数据
        # self.truncate_table()

    # 清空数据表
    def truncate_table(self):
        try:
            truncate_table_sql = "TRUNCATE TABLE stock_info;" \
                                 "TRUNCATE TABLE stock_market;" \
                                 "TRUNCATE TABLE stock_dividend;" \
                                 "TRUNCATE TABLE stock_share_holder" \
                                 "TRUNCATE TABLE stock_index;"
            self.cursor.execute(truncate_table_sql)
            self.conn.commit()
            # 关闭连接
            self.close_conn()
        except pymysql.Error as err:
            # 事务回滚
            self.conn.rollback()
            print("OS error: {0}".format(err))
            raise

    # 默认处理item
    def process_item(self, item, spider):
        if item.__class__ == StockIndexItem:
            self.insertStockIndex(item)
            # raise DropItem("This item has scrpyed.")
        if item.__class__ == StockInfoItem:
            self.insertStockInfo(item)
            # raise DropItem("This item has scrpyed.")
        if item.__class__ == StockMarketItem:
            self.insertStockMarket(item)
            # raise DropItem("This item has scrpyed.")
        if item.__class__ == StockDividendItem:
            self.insertStockDividend(item)
            # raise DropItem("This item has scrpyed.")
        if item.__class__ == StockShareHolderItem:
            self.insertStockShareHolder(item)
        return item

    # 插入股票大盘信息表
    def insertStockIndex(self, item):
        try:
            query_sql = """select COUNT(1) from stock_index where index_name = %s"""
            print("===判断股票大盘信息sql:" + query_sql)

            # 执行SQL查询语句
            self.cursor.execute(query_sql, item['index_name'].encode('utf-8'))
            # 获取列表记录条数
            count = self.cursor.fetchone()
            if (int(count[0]) > 0):
                return

            # 没有就插入
            insert_sql = """INSERT INTO stock_index(index_code, index_name, create_time)VALUES(%s, %s, %s)"""

            print("===插入股票大盘信息sql:" + insert_sql)
            self.cursor.execute(insert_sql, (
                item['index_code'],
                item['index_name'].encode('utf-8'),
                item['create_time']
            ))

            # 事务提交
            self.conn.commit()
        except pymysql.Error as err:
            # 事务回滚
            self.conn.rollback()
            print("OS error: {0}".format(err))
            raise

    # 插入股票基本信息表
    def insertStockInfo(self, item):
        try:
            # 首先根据股票编码查询数据库中是否已经存在（即先前已经成功爬取过）
            query_sql = """SELECT id FROM stock_info WHERE stock_code = %s"""
            self.cursor.execute(query_sql, item['stock_code'][0].encode('utf-8'))

            print("===判断股票基本信息sql:" + query_sql)
            result = self.cursor.fetchone()

            if result is not None and len(result) > 0:
                # 存在就修改
                update_sql = """UPDATE stock_info SET last_trade = %s WHERE id = %s"""

                print("===修改股票基本信息sql:" + update_sql)
                self.cursor.execute(update_sql, item['last_trade'][0].encode('utf-8'), result[0])
            else:
                # 不存在直接插入
                insert_sql = """INSERT INTO stock_info(stock_code, stock_name, index_code,
                                last_trade, create_time)VALUES(%s, %s, %s, %s, %s)"""

                print("===修改股票基本信息sql:" + insert_sql)
                self.cursor.execute(insert_sql, (
                    item['stock_code'][0].encode('utf-8'),
                    item['stock_name'][0].encode('utf-8'),
                    item['index_code'],
                    item['last_trade'][0].encode('utf-8'),
                    item['create_time']
                ))

            # 事务提交
            self.conn.commit()
        except pymysql.Error as err:
            # 事务回滚
            self.conn.rollback()
            print("OS error: {0}".format(err))
            raise

    # 插入股票历史行情信息表
    def  insertStockMarket(self, item):
        try:
            # 根据股票编码查询之前是否已经爬取过
            query_sql = """select count(1) from stock_market where stock_code = %s and trade_date = %s"""
            self.cursor.execute(query_sql, (
                                item['stock_code'][0].encode('utf-8'),
                                item['trade_date'][0].encode('utf-8')))

            print("===判断历史行情sql:" + query_sql)
            count = self.cursor.fetchone()
            if (int(count[0]) >= 1):
                return

            # 没有就插入
            insert_sql = """INSERT INTO stock_market(stock_code, stock_name, trade_date, stock_open, high, low, stock_close,
                volumn, turnover, create_time)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            print("===插入历史行情sql:" + insert_sql)
            self.cursor.execute(insert_sql, (
                item['stock_code'].encode('utf-8'),
                item['stock_name'].encode('utf-8'),
                item['trade_date'][0].encode('utf-8'),
                item['stock_open'][0].encode('utf-8'),
                item['high'][0].encode('utf-8'),
                item['low'][0].encode('utf-8'),
                item['stock_close'][0].encode('utf-8'),
                item['volumn'][0].encode('utf-8'),
                item['turnover'][0].encode('utf-8'),
                item['create_time']
            ))

            # 事务提交
            self.conn.commit()
        except pymysql.Error as err:
            # 事务回滚
            self.conn.rollback()
            print("OS error: {0}".format(err))
            raise

    # 插入股票分红配送记录表
    def insertStockDividend(self, item):
        try:
            # 先查询先前是否已抓取过
            query_sql = """select count(1) from stock_dividend where stock_code = %s and ex_dividend_date = %s and bonus_year = %s"""
            self.cursor.execute(query_sql, (
                                item['stock_code'][0].encode('utf-8'),
                                item['ex_dividend_date'],
                                item['bonus_year']))

            print("===判断股票分红sql:" + query_sql)
            count = self.cursor.fetchone()
            if (int(count[0]) >= 1):
                return

            # 如果先前没有抓取过，就直接插入
            insert_sql = """INSERT INTO stock_dividend(stock_code, stock_name, ex_dividend_date, bonus_year, dividend_value,
                    conversion_value, create_time, dividend_mark) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

            print("===插入股票分红sql:" + insert_sql)

            self.cursor.execute(insert_sql, (
                item['stock_code'],
                item['stock_name'].encode('utf-8'),
                item['ex_dividend_date'],
                item['bonus_year'],
                item['dividend_value'],
                item['conversion_value'],
                item['create_time'],
                item['dividend_mark']
            ))

            # 事务提交
            self.conn.commit()
        except pymysql.Error as err:
            # 事务回滚
            self.conn.rollback()
            print("OS error: {0}".format(err))
            raise

    # 插入股票股东股本信息表
    def insertStockShareHolder(self, item):
        try:
            insert_sql = """INSERT INTO stock_share_holder(stock_code, stock_name, holder_rank, holder_name, hold_count,
                hold_rate, freezing_count, pledged_count, create_time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""

            print("===插入股票股东股本sql:" + insert_sql)
            self.cursor.execute(insert_sql, (
                item['stock_code'],
                item['stock_name'].encode('utf-8'),
                item['holder_rank'],
                item['holder_name'],
                item['hold_count'],
                item['hold_rate'],
                item['freezing_count'],
                item['pledged_count'],
                item['create_time']
            ))

            # 事务提交
            self.conn.commit()
        except pymysql.Error as err:
            # 事务回滚
            self.conn.rollback()
            print("OS error: {0}".format(err))
            raise

    # 关闭数据库连接
    def close_conn(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()
