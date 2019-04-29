# 8btc_scraper
这是一个针对[巴比特论坛](http://8btc.com/forum-2-1.html)设计的爬虫程式。

*其他语言版本: [English](README.md), [繁體中文](README.zh-tw.md)， [简体中文](README.zh-cn.md).*

## 构想和目的
在用户发帖内容中提取情绪词语，构建情绪指标，与比特币期货走势拟合，构建择时策略。

## 爬取讯息
1. 文章名称
2. 评论数
3. 阅览数
3. 发布日期
4. 正面字出现次数 {好，涨，红，赚}
5. 负面字出现次数 {差，跌，熊，绿，亏}

## 使用工具
Python 2.7, BeautifulSoup4
