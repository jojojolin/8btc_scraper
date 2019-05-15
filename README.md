# 8btc_scraper
This is a web scraper designed for the [8btc](http://8btc.com/forum-2-1.html)  forum.

*Read this in other languages: [English](README.md), [繁體中文](README.zh-tw.md)， [简体中文](README.zh-cn.md).*

## Motivation
Extract emotional sentiments from posts and comments to construct sentimental index, which could then be used as a reference for predicting bitcoin prices and making decisions.

## Information Extracted
1. Title of the article
2. Number of comments
3. Number of views
3. Date of publish
4. Positive word count {好(good)，涨(rise/soar/surge)，红(red)，赚(profit)}
5. Negative word count {差(bad)，跌(drop/fall/dip)，熊(bear)，绿(green)，亏(deficit)}

## Technologies
Python 2.7, BeautifulSoup4