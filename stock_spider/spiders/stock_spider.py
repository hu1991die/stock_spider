# encoding: utf-8
'''
@author: feizi
@file: stock_spider.py
@time: 2017/9/10 10:06
@Software: PyCharm
@desc:
'''

import re

from scrapy import Request
from scrapy.spiders import Spider

from stock_spider.items import StockDividendItem
from stock_spider.items import StockIndexItem
from stock_spider.items import StockInfoItem
from stock_spider.items import StockMarketItem
from stock_spider.items import StockShareHolderItem
from stock_spider.items import StockTypeItem
from stock_spider.utils.CommonUtil import CommonUtil


# 股票信息爬虫Spider
class StockSpider(Spider):
    # 禁止DEBUG级别的日志
    # logging.disable(logging.DEBUG)

    # 爬虫的名称
    name = "stock_spider"
    # 允许爬取的域名，非此域名的网页不会爬取
    allowed_domains = ["finance.ifeng.com", "vip.stock.finance.sina.com.cn"]

    # 基础url
    base_url = "http://app.finance.ifeng.com/list/stock.php"
    # 股票历史行情url
    detail_url = "http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/%s.phtml?year=%d&jidu=%d"
    # 分红派息记录url
    dividend_url = "http://app.finance.ifeng.com/data/stock/tab_fhpxjl.php?symbol=%s"
    # 股票股本信息url
    holder_url = "http://app.finance.ifeng.com/data/stock/tab_gdgb.php?symbol=%s"
    # 股票所属板块信息url
    stock_type_url = "http://finance.ifeng.com/app/hq/stock/sh%s/index.shtml"

    start_urls = [
        base_url
    ]

    def __init__(self):
        self.commonUtil = CommonUtil()

    # 获取凤凰财经网站股票模块50页信息网址
    def parse(self, response):
        # 大盘编码
        index_code = self.commonUtil.createUUID()
        # print("大盘编码：" + index_code)

        print("=======抓取大盘信息基础base_url：" + self.base_url)
        yield Request(url=self.base_url, meta={'index_code': index_code},
                      callback=self.parseStockIndex)

        # 提取沪市A股下面所有的上市股票信息列表
        page_url = "?t=ha&f=chg_pct&o=desc&p="
        for i in range(1, 2):
            url = self.base_url + page_url + str(i)
            print("=======提取沪市A股下面所有的上市股票信息列表url：" + url)
            yield Request(url=url, meta={'index_code': index_code},
                          callback=self.parseStockInfo)

    # 抓取大盘基本信息
    def parseStockIndex(self, response):
        # 页面主要内容
        main_content = response.css(".main > div.content")
        # print(main_content)

        # 大盘编码
        index_code = response.meta['index_code']
        # print(index_code)

        # 大盘名称
        index_name = main_content.css(".block").xpath("//h1/text()").extract_first()
        # print("大盘名称：" + index_name)

        # 创建时间
        create_time = self.commonUtil.getCreateTime()
        # print("创建时间：" + create_time)

        # 定义大盘基本信息item
        stock_index_item = StockIndexItem()
        stock_index_item['index_code'] = index_code
        stock_index_item['index_name'] = index_name
        stock_index_item['create_time'] = create_time
        pass
        yield stock_index_item

    # 抓取大盘下面的股票列表
    def parseStockInfo(self, response):
        stock_sets = set()

        # 主要内容
        main_content = response.css(".main > div.content")
        # print(main_content)

        # 大盘编码
        index_code = response.meta['index_code']
        # print(index_code)

        stockInfoList = main_content.css(".block02 > div.tab01").xpath("//table/tr[position() > 1 and position() < 52]")
        # print("股票列表：\n")
        for stockInfo in stockInfoList:
            if (len(stockInfo.xpath("td").extract()) < 3):
                continue

            # 股票代码
            stock_code = stockInfo.xpath("td[1]/a/text()").extract()
            # 股票名称
            stock_name = stockInfo.xpath("td[2]/a/text()").extract()
            # 当前最新价格
            last_trade = stockInfo.xpath("td[3]/span/text()").extract()
            # 创建时间
            create_time = CommonUtil().getCreateTime()

            # 打印输出
            print(stock_code, stock_name, index_code, last_trade, create_time)

            # 定义大盘基本信息item
            stock_info_item = StockInfoItem()
            stock_info_item['stock_code'] = stock_code
            stock_info_item['stock_name'] = stock_name
            stock_info_item['index_code'] = index_code
            stock_info_item['last_trade'] = last_trade
            stock_info_item['create_time'] = create_time

            stock_sets.add(stock_info_item)
            pass
            yield stock_info_item

        # 循环股票列表数据，提取每只股票的股东股本信息
        for stock_info in stock_sets:
            stock_code = stock_info['stock_code'][0]
            stock_name = stock_info['stock_name'][0]

            # 提取股票股东股本信息的url
            holder_url = self.holder_url % stock_code
            print("======提取股票股东股本信息holder_url:" + holder_url)
            yield Request(url=holder_url, meta={'stock_code': stock_code, 'stock_name': stock_name},
                          callback=self.parsestockShareHolder)

        # 循环股票列表数据,提取股票分红信息
        for stock_info in stock_sets:
            stock_code = stock_info['stock_code'][0]
            stock_name = stock_info['stock_name'][0]

            # 提取股票分红配送记录信息
            dividend_url = self.dividend_url % stock_code
            print("======提取股票分红配送记录信息dividend_url:" + dividend_url)
            yield Request(url=dividend_url, meta={'stock_code': stock_code, 'stock_name': stock_name},
                          callback=self.parseStockDividendRecord)

        # 循环股票列表数据,提取股票所属板块（标签）信息
        for stock_info in stock_sets:
            stock_code = stock_info['stock_code'][0]
            stock_name = stock_info['stock_name'][0]

            # 提取股票所属板块信息
            stock_type_url = self.stock_type_url % stock_code
            print("======提取股票所属板块信息stock_type_url:" + stock_type_url)
            yield Request(url=stock_type_url, meta={'stock_code': stock_code, 'stock_name': stock_name},
                          callback=self.parseStockTypeData)

        # 循环股票列表数据，提取股票历史记录行情信息
        for stock_info in stock_sets:
            stock_code = stock_info['stock_code'][0]
            stock_name = stock_info['stock_name'][0]

            # 循环从1990到2017年
            for year in range(2017, 2018):
                # 每年四个季度
                for quarter in range(1, 2):
                    data_url = self.detail_url % (stock_code, year, quarter)
                    print("======提取股票历史记录行情信息data_url：" + data_url)
                    yield Request(url=data_url, meta={'stock_code': stock_code, 'stock_name': stock_name, 'year': year},
                                  callback=self.parseHistoryStockData)

    # 爬取股票股东股本信息
    def parsestockShareHolder(self, response):
        # 股票代码
        stock_code = response.meta['stock_code']
        # 股票名称
        stock_name = response.meta['stock_name']

        # 解析股票股本页面信息
        div_content = response.xpath("//div[@class='Rtbox']")
        if div_content is None:
            return

        # 股东股本信息列表
        table = div_content.xpath("table[@class='tab01']")
        if table is None:
            return

        # 股东股本信息每一列
        tr_list = table.xpath(".//tr[position() > 3]")
        if tr_list is None:
            return

        # 循环tr_list列表
        for tr in tr_list:
            # 股东名次
            holder_rank = tr.xpath(".//td[1]/text()").extract_first()
            # 股东名称
            holder_name = tr.xpath(".//td[2]/text()").extract_first()
            # 持有数量(股)
            hold_count = tr.xpath(".//td[3]/text()").extract_first()
            # 持有比例(%)
            hold_rate = tr.xpath(".//td[4]/text()").extract_first()
            # 冻结数量
            freezing_count = tr.xpath(".//td[4]/text()").extract_first()
            # 质押数量
            pledged_count = tr.xpath(".//td[4]/text()").extract_first()
            # 创建时间
            create_time = CommonUtil().getCreateTime()

            # 构建item
            holder_item = StockShareHolderItem()
            holder_item['stock_code'] = stock_code
            holder_item['stock_name'] = stock_name
            holder_item['holder_rank'] = holder_rank
            holder_item['holder_name'] = holder_name
            holder_item['hold_count'] = hold_count
            holder_item['hold_rate'] = hold_rate
            holder_item['freezing_count'] = freezing_count
            holder_item['pledged_count'] = pledged_count
            holder_item['create_time'] = create_time
            pass
            yield holder_item

    # 爬取股票分红派息记录数据
    def parseStockDividendRecord(self, response):
        # 股票代码
        stock_code = response.meta['stock_code']
        # 股票名称
        stock_name = response.meta['stock_name']

        # 抓取分红派息记录数据
        div_content = response.xpath("//div[@class='Right770 clearfix']")
        if div_content is None:
            return

        # 分红派息记录列表
        table_list = div_content.xpath("table[@class='tab01']")
        if table_list is None:
            return

        # 循环table_list列表
        for table in table_list:
            # 除权出息日
            ex_dividend_date = table.xpath(".//tr[5]/td[4]/text()").extract_first()
            # 分红年度
            bonus_year = table.xpath(".//tr[1]/td[4]/text()").extract_first()
            # 派息值
            dividend_value = table.xpath(".//tr[3]/td[4]/text()").extract_first()
            # 转股值
            conversion_value = table.xpath(".//tr[4]/td[4]/text()").extract_first()
            # 创建时间
            create_time = CommonUtil().getCreateTime()

            # 判空处理
            if dividend_value is None:
                dividend_value = 0
            else:
                dividend_value = float(re.findall(r'([0-9.]+)', dividend_value, re.MULTILINE)[0]) / 10

            if conversion_value is None:
                conversion_value = 0
            else:
                conversion_value = float(re.findall(r'([0-9.]+)', conversion_value, re.MULTILINE)[0]) / 10

            # 分红标志
            if dividend_value == 0 and conversion_value == 0:
                dividend_mark = 0
            else:
                dividend_mark = 1

            dividend_item = StockDividendItem()
            dividend_item['stock_code'] = stock_code
            dividend_item['stock_name'] = stock_name
            dividend_item['ex_dividend_date'] = ex_dividend_date
            dividend_item['bonus_year'] = bonus_year
            dividend_item['dividend_value'] = dividend_value
            dividend_item['conversion_value'] = conversion_value
            dividend_item['create_time'] = create_time
            dividend_item['dividend_mark'] = dividend_mark
            pass
            yield dividend_item

    # 爬取历史行情数据
    def parseHistoryStockData(self, response):
        stock_code = response.meta['stock_code']
        stock_name = response.meta['stock_name']
        year = response.meta['year']

        # 抓取历史行情数据内容
        content = response.xpath("//div[@id='center']").xpath(".//table[@id='FundHoldSharesTable']")
        if content is None:
            return

        # 抓取行情列表
        trs = content.xpath("tr[position() > 1]")
        if trs is None:
            return

        # 循环行情列表
        for tr in trs:
            # 交易日期
            if (year < 2007):
                trade_date = tr.xpath("normalize-space(td[1]/div/text())").extract()
            else:
                trade_date = tr.xpath("normalize-space(td[1]/div/a/text())").extract()

            # 今开盘价格
            stock_open = tr.xpath("normalize-space(td[2]/div/text())").extract()
            # 最高价格
            high = tr.xpath("normalize-space(td[3]/div/text())").extract()
            # 昨收盘价格
            stock_close = tr.xpath("normalize-space(td[4]/div/text())").extract()
            # 最低价格
            low = tr.xpath("normalize-space(td[5]/div/text())").extract()
            # 成交量
            volumn = tr.xpath("normalize-space(td[6]/div/text())").extract()
            # 成交额
            turnover = tr.xpath("normalize-space(td[7]/div/text())").extract()

            # 创建时间
            create_time = CommonUtil().getCreateTime()
            print(trade_date, stock_open, high, stock_close, low, volumn, turnover, create_time)

            market_item = StockMarketItem()
            market_item['stock_code'] = stock_code
            market_item['stock_name'] = stock_name
            market_item["trade_date"] = trade_date
            market_item["stock_open"] = stock_open
            market_item["high"] = high
            market_item["low"] = low
            market_item["stock_close"] = stock_close
            market_item["volumn"] = volumn
            market_item["turnover"] = turnover
            market_item["create_time"] = create_time

            pass
            yield market_item

    # 爬取股票所属板块信息数据
    def parseStockTypeData(self, response):
        # 股票代码
        stock_code = response.meta['stock_code']
        # 股票名称
        stock_name = response.meta['stock_name']

        # 抓取股票所属板块分类信息
        div_content = response.xpath("//div[@class='picForme']")
        if div_content is None:
            return

        # 抓取股票所属板块分类信息table
        table_conent = div_content.xpath("table[@class='tabPic']/tr[position() = 3]")
        if table_conent is None:
            return

        # 提取股票分类标签信息所在的a标签列表
        typeList = table_conent.xpath("td[@class='lastBot']/span/a")
        if typeList is None:
            return

        # 循环a标签列表，提取标签编码信息和文本信息
        for type in typeList:
            # 股票标签编码code
            stock_type_code = type.xpath(".//@href").extract_first()
            stock_type_code = re.sub("\D", "", stock_type_code)
            # 股票标签编码名称
            stock_type = type.xpath(".//text()").extract_first()
            # 创建时间
            create_time = CommonUtil().getCreateTime()

            # 打印
            print(stock_code, stock_name, stock_type_code, stock_type, create_time)

            stock_type_item = StockTypeItem()
            stock_type_item['stock_code'] = stock_code
            stock_type_item['stock_name'] = stock_name
            stock_type_item['stock_type_code'] = stock_type_code
            stock_type_item['stock_type'] = stock_type
            stock_type_item['create_time'] = create_time

            pass
            yield stock_type_item



