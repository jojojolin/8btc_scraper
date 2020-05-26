# 8btc_scraper
這是一個針對[鏈節點](https://www.chainnode.com/forum-2-1.html)所設計的爬蟲程式。

*其他語言版本: [English](README.md), [繁體中文](README.zh-tw.md)， [简体中文](README.zh-cn.md).*

## 構想
從用戶發帖內容中提取情緒詞語，構建情緒指標，與比特幣期貨走勢擬合，從而構建選擇的策略。

## 爬取的訊息
1. 文章名稱
2. 評論數
3. 閱覽數
3. 發布日期
4. 正面字出現次數 {好，漲，紅，賺}
5. 負面字出現次數 {差，跌，熊，綠，虧}

## 事先需要安裝
Python 3, pip

## 執行腳本前
在clone好的 8btc 文件夾裡:
1. 創建一個虛擬的python環境，在terminal裡面跑 `virtualenv venv`
2. 然後，執行  `source venv/bin/activate` 完成激活
3. 最後，執行  `pip install -r requirements.txt` 來完成所有依賴庫的安裝

# 跑腳本
1. `python scraper.py`

# 事後清理
1.關閉虛擬python環境，在terminal裡執行  `deactivate` 
