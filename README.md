# 8btc_scraper
This is a web scraper designed for the [ChainNode](https://www.chainnode.com/forum-2-1.html)  forum.

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

## Prerequisites
Python 3, pip

## Before running the script
In your cloned 8btc folder:
1. Create a virtual environment folder by running `virtualenv venv`
2. Activate venv by running `source venv/bin/activate`
3. Now run `pip install -r requirements.txt`

# Run the script
1. `python scraper.py`

# After running
1. Deactivate the env by running `deactivate`