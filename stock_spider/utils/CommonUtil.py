# encoding: utf-8
'''
@author: feizi
@file: CommonUtil.py
@time: 2017/4/16 21:03
@Software: PyCharm
@desc:
'''

import datetime
import re
import uuid


# 统一工具类
class CommonUtil(object):
    def __init__(self):
        return

    # 生成UUID唯一性主键值
    def createUUID(self):
        return str(uuid.uuid1())

    # 生成日期时间
    def getCreateTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 提取数字(浮点型)
    def extract_digit(value):
        if value is not None:
            value = re.findall(r'([0-9.]+)', value, re.MULTILINE)[0]
            return float(value) / 10
        else:
            return 0
