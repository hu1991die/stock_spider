# encoding: utf-8
'''
@author: feizi
@file: main.py
@time: 2017/9/10 9:56
@Software: PyCharm
@desc:
'''

from scrapy import cmdline

cmdline.execute("scrapy crawl stock_spider".split())