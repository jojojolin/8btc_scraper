# 8btc_scraper
这是一个针对[链节点](https://www.chainnode.com/forum-2-1.html)设计的爬虫程式。

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

## 事先需要安装
Python 3, pip

## 执行脚本前
在clone好的 8btc 文件夹里:
1. 建造一个虚拟的python环境，在终端机中执行 `virtualenv venv`
2. 之后，执行  `source venv/bin/activate` 以激活它
3. 最后，执行  `pip install -r requirements.txt` 来完成所有依赖的库的安装

# 运行脚本
1. `python scraper.py`

# 事后清理
1.关闭虚拟环境功能，使用命令  `deactivate`