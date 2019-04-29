# 8btc_scraper
This is a web scraper designed for the [8btc](http://8btc.com/forum-2-1.html)  forum.

*Read this in other languages: [English](README.md), [繁體中文](README.zh-tw.md)， [简体中文](README.zh-cn.md).*

## Objective
Extract emotional sentiment from user posts to construct sentimental index, which could then be used for predicting bitcoin stock prices and decision making.

## Information Extracted
1. Title of the article
2. Number of comments
3. Number of views
3. Date of publish
4. Positive word count {好，涨，红，赚}
5. Negative word count {差，跌，熊，绿，亏}

## Technologies
Python 2.7, BeautifulSoup4
