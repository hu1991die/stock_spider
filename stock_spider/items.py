# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item

'''股票基本信息'''
class StockInfoItem(Item):
    # 股票代码
    stock_code = Field()
    # 股票名称
    stock_name = Field()
    # 股票大盘编码
    index_code = Field()
    # 当前最新交易价格
    last_trade = Field()
    # 公司名称
    company_name = Field()
    # 公司股票上市日期
    launch_date = Field()
    # 创建时间
    create_time = Field()


'''股票大盘信息表'''
class StockIndexItem(Item):
    # 大盘编码
    index_code = Field()
    # 大盘名称
    index_name = Field()
    # 创建时间
    create_time = Field()


'''股票交易行情'''
class StockMarketItem(Item):
    # 股票代码
    stock_code = Field()
    # 股票名称
    stock_name = Field()
    # 交易日期
    trade_date = Field()
    # 涨跌幅
    chg = Field()
    # 涨跌额
    stock_change = Field()
    # 今开盘价格
    stock_open = Field()
    # 昨收盘价格
    stock_close = Field()
    # 最高价格
    high = Field()
    # 最低价格
    low = Field()
    # 成交量
    volumn = Field()
    # 成交额
    turnover = Field()
    # 换手率
    turnover_rate = Field()
    # 市盈率
    price_earing_rate = Field()
    # 流通市值
    market_value = Field()
    # 总市值
    total_value = Field()
    # 每股收益
    earning_per_share = Field()
    # 净利润
    net_profit = Field()
    # 主营收
    main_revenue = Field()
    # 创建时间
    create_time = Field()


'''股票分红配送记录'''
class StockDividendItem(Item):
    # 股票代码
    stock_code = Field()
    # 股票名称
    stock_name = Field()
    # 除权出息日
    ex_dividend_date = Field()
    # 分红年度
    bonus_year = Field()
    # 派息值
    dividend_value = Field()
    # 转股值
    conversion_value = Field()
    # 创建时间
    create_time = Field()
    # 分红标志
    dividend_mark = Field()


'''股东股本信息'''
class StockShareHolderItem(Item):
    # 股票代码
    stock_code = Field()
    # 股票名称
    stock_name = Field()
    # 股东名次
    holder_rank = Field()
    # 股东名称
    holder_name = Field()
    # 持有数量(股)
    hold_count = Field()
    # 持有比例(%)
    hold_rate = Field()
    # 冻结数量
    freezing_count = Field()
    # 质押数量
    pledged_count = Field()
    # 创建时间
    create_time = Field()


'''股票综合指数信息表'''
class StockCompositeIndexItem(Item):
    # 指数代码
    index_code = Field()
    # 指数名称
    index_name = Field()
    # 当前价
    last_trade = Field()
    # 涨跌额
    index_change = Field()
    # 涨跌幅
    chg = Field()
    # 现手
    now_hands = Field()
    # 总手
    total_hands = Field()
    # 成交金额
    turnover = Field()
    # 今开盘
    index_open = Field()
    # 昨收盘
    index_close = Field()
    # 创建时间
    create_time = Field()


'''股票综合指数历史涨跌行情信息表'''
class StockCompositeIndexHistoryItem(Item):
    # 指数代码
    index_code = Field()
    # 指数名称
    index_name = Field()
    # 开盘
    opening = Field()
    # 收盘
    closing = Field()
    # 涨跌额
    index_change = Field()
    # 涨跌幅
    chg = Field()
    # 最低
    lowest = Field()
    # 最高
    highest = Field()
    # 成交量(手)
    volumn = Field()
    # 成交金额(万)
    turnover = Field()
    # 交易日期
    trade_date = Field()
    # 创建时间
    create_time = Field()
