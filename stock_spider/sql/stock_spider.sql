/*
Navicat MySQL Data Transfer

Source Server         : loclahost
Source Server Version : 50635
Source Host           : localhost:3306
Source Database       : stock_spider

Target Server Type    : MYSQL
Target Server Version : 50635
File Encoding         : 65001

Date: 2017-09-10 22:26:11
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for stock_composite_index
-- ----------------------------
DROP TABLE IF EXISTS `stock_composite_index`;
CREATE TABLE `stock_composite_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `index_code` varchar(20) DEFAULT NULL COMMENT '指数代码',
  `index_name` varchar(20) DEFAULT NULL COMMENT '指数名称',
  `last_trade` decimal(14,2) DEFAULT NULL COMMENT '当前价',
  `index_change` decimal(14,2) DEFAULT NULL COMMENT '涨跌额',
  `chg` varchar(20) DEFAULT NULL COMMENT '涨跌幅',
  `now_hands` int(11) DEFAULT NULL COMMENT '现手',
  `total_hands` int(11) DEFAULT NULL COMMENT '总手',
  `turnover` varchar(20) DEFAULT NULL COMMENT '成交金额',
  `index_open` decimal(14,2) DEFAULT NULL COMMENT '今开盘',
  `index_close` decimal(14,2) DEFAULT NULL COMMENT '昨收盘',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='股票综合指数行情信息表';

-- ----------------------------
-- Table structure for stock_composite_index_history
-- ----------------------------
DROP TABLE IF EXISTS `stock_composite_index_history`;
CREATE TABLE `stock_composite_index_history` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `index_code` varchar(20) DEFAULT NULL COMMENT '指数代码',
  `index_name` varchar(20) DEFAULT NULL COMMENT '指数名称',
  `opening` decimal(14,2) DEFAULT NULL COMMENT '开盘',
  `closing` decimal(14,2) DEFAULT NULL COMMENT '收盘',
  `index_change` decimal(14,2) DEFAULT NULL COMMENT '涨跌额',
  `chg` varchar(20) DEFAULT NULL COMMENT '涨跌幅',
  `lowest` decimal(14,2) DEFAULT NULL COMMENT '最低',
  `highest` decimal(14,2) DEFAULT NULL COMMENT '最高',
  `volumn` varchar(20) DEFAULT NULL COMMENT '成交量(手)',
  `turnover` varchar(20) DEFAULT NULL COMMENT '成交金额(万)',
  `trade_date` datetime DEFAULT NULL COMMENT '交易日期',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='股票综合指数历史涨跌行情信息表';

-- ----------------------------
-- Table structure for stock_dividend
-- ----------------------------
DROP TABLE IF EXISTS `stock_dividend`;
CREATE TABLE `stock_dividend` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `stock_code` varchar(20) NOT NULL COMMENT '股票代码',
  `stock_name` varchar(20) DEFAULT NULL COMMENT '股票名称',
  `ex_dividend_date` varchar(20) DEFAULT NULL COMMENT '除权除息日',
  `bonus_year` varchar(20) DEFAULT NULL COMMENT '分红年度',
  `dividend_value` varchar(20) DEFAULT NULL COMMENT '派息值',
  `conversion_value` varchar(20) DEFAULT NULL COMMENT '转股值',
  `create_time` date DEFAULT NULL COMMENT '创建时间',
  `dividend_mark` tinyint(4) DEFAULT '0' COMMENT '分红标志',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=271 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for stock_index
-- ----------------------------
DROP TABLE IF EXISTS `stock_index`;
CREATE TABLE `stock_index` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `index_code` varchar(40) NOT NULL COMMENT '大盘编码',
  `index_name` varchar(40) DEFAULT NULL COMMENT '大盘名称',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for stock_info
-- ----------------------------
DROP TABLE IF EXISTS `stock_info`;
CREATE TABLE `stock_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `stock_code` varchar(20) NOT NULL COMMENT '股票代码',
  `stock_name` varchar(40) DEFAULT NULL COMMENT '股票名称',
  `index_code` varchar(60) DEFAULT NULL COMMENT '大盘编码',
  `last_trade` decimal(14,2) DEFAULT NULL COMMENT '当前最新交易价格',
  `company_name` varchar(40) DEFAULT NULL COMMENT '公司名称',
  `launch_date` date DEFAULT NULL COMMENT '上市日期',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for stock_market
-- ----------------------------
DROP TABLE IF EXISTS `stock_market`;
CREATE TABLE `stock_market` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键Id',
  `stock_code` varchar(20) NOT NULL COMMENT '股票代码',
  `stock_name` varchar(20) DEFAULT NULL COMMENT '股票名称',
  `trade_date` date DEFAULT NULL COMMENT '交易日期',
  `chg` varchar(20) DEFAULT NULL COMMENT '涨跌幅',
  `stock_change` decimal(14,2) DEFAULT NULL COMMENT '涨跌额',
  `stock_open` decimal(14,2) DEFAULT NULL COMMENT '今开盘价格',
  `stock_close` decimal(14,2) DEFAULT NULL COMMENT '昨收盘价格',
  `high` decimal(14,2) DEFAULT NULL COMMENT '最高价格',
  `low` decimal(14,2) DEFAULT NULL COMMENT '最低价格',
  `volumn` varchar(20) DEFAULT NULL COMMENT '成交量',
  `turnover` varchar(20) DEFAULT NULL COMMENT '成交额',
  `turnover_rate` varchar(20) DEFAULT NULL COMMENT '换手率',
  `price_earing_rate` varchar(20) DEFAULT NULL COMMENT '市盈率',
  `market_value` varchar(20) DEFAULT NULL COMMENT '流通市值',
  `total_value` varchar(20) DEFAULT NULL COMMENT '总市值',
  `earning_per_share` decimal(14,2) DEFAULT NULL COMMENT '每股收益',
  `net_profit` varchar(20) DEFAULT NULL COMMENT '净利润',
  `main_revenue` varchar(20) DEFAULT NULL COMMENT '主营收',
  `create_time` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  KEY `idx_stock_code` (`stock_code`)
) ENGINE=InnoDB AUTO_INCREMENT=2064 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for stock_share_holder
-- ----------------------------
DROP TABLE IF EXISTS `stock_share_holder`;
CREATE TABLE `stock_share_holder` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `stock_code` varchar(20) DEFAULT NULL COMMENT '股票代码',
  `stock_name` varchar(40) DEFAULT NULL COMMENT '股票名称',
  `holder_rank` char(2) DEFAULT NULL COMMENT '股东名次',
  `holder_name` varchar(40) DEFAULT NULL COMMENT '股东名称',
  `hold_count` int(11) DEFAULT NULL COMMENT '持有数量(股)',
  `hold_rate` decimal(10,4) DEFAULT NULL COMMENT '持有比例(%)',
  `freezing_count` int(11) DEFAULT NULL COMMENT '冻结数量',
  `pledged_count` int(11) DEFAULT NULL COMMENT '质押数量',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=466 DEFAULT CHARSET=utf8 COMMENT='股东股本信息表';
