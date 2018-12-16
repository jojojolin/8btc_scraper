# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import execjs
import re
import requests
import csv

# 用于HTTP的GET请求头
HEADERS = {
#    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#    'Accept-Encoding': 'gzip, deflate, sdch',
#    'Accept-Language':'zh-CN,zh;q=0.8',
#    'AlexaToolbar-ALX_NS_PH': 'AlexaToolbar/alx-4.0',
#    'Cache-Control': 'max-age=0',
#    'Connection':'keep-alive',
#    "Host": "8btc.com",
#    'Referer':'http://8btc.com/',
#    #'Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
}

# 正面的情绪字
POSITIVES = ['好'.decode('utf-8'),
             '涨'.decode('utf-8'),
             '牛'.decode('utf-8'),
             '红'.decode('utf-8'),
             '赚'.decode('utf-8')]

# 负面的情绪字
NEGATIVES = ['差'.decode('utf-8'),
             '跌'.decode('utf-8'),
             '熊'.decode('utf-8'),
             '绿'.decode('utf-8'),
             '亏'.decode('utf-8')]


# 用于在python里执行JS的函数    
def executejs(html):
    # 提取其中的JS加密函数
    js_string = ''.join(re.findall(r'(function .*?)</script>',html))

    # 提取其中执行JS函数的参数
    js_func_arg = re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', html)[0]
    js_func_name = re.findall(r'function (\w+)',js_string)[0]

    # 修改JS函数，使其返回Cookie内容
    js_string = js_string.replace('eval("qo=eval;qo(po);")', 'return po')

    func = execjs.compile(js_string)
    return func.call(js_func_name,js_func_arg)


# 用于整理cookie格式的函数
def parse_cookie(string):
    string = string.replace("document.cookie='", "")
    clearance = string.split(';')[0]
    return {clearance.split('=')[0]: clearance.split('=')[1]}


# 从回复的头里取得cookie讯息的函数，用于反爬虫网站
def getCookie(theUrl):
    # 第一次访问获取动态加密的JS
    req = requests.get(url=theUrl,headers=HEADERS)
    first_html = req.content.decode('UTF-8')
    # 执行JS获取Cookie
    cookie_str = executejs(first_html)
    # 将Cookie转换为字典格式
    cookie = parse_cookie(cookie_str)
    cookie_id = req.cookies
    cookie_id = '; '.join(['='.join(item) for item in cookie_id.items()])
    return (cookie_id, cookie.keys()[0]+"="+cookie.values()[0])


def main():
    # 定义变量
    data =[] # 储存结果的容器
    offset = 1 # 记录论坛的当前页数
    url = 'http://8btc.com/forum-2-'+str(offset)+'.html'
    data.append(('文章名称'.decode('utf-8'),'评论数','阅览数','发布日期','正面字','负面字'))
    # 从第一次普通访问截取cookie
    cookies = getCookie(url)
    setCookie = cookies[0]+';'+cookies[1]
    # 将截取到的两个cookies加入到以后请求的头里
    HEADERS.update({'Cookie':setCookie})
    
    #循环一直到最后一页（pg 1000）
    while offset < 1001:
        html=requests.get(url,
                          headers=HEADERS).text
        soup = BeautifulSoup(html, 'html.parser')

        post_divs = soup.find_all('a',attrs={'class':'s xst'})

        for div in post_divs:
            #div.prettify('gb18030')
            #div.encode('gb18030')
            positive = 0
            negative = 0
            # 文章名称
            name = div.get_text()
            # 获取文章链接
            link = div.get('href')
            # 进入文章链接
            html = requests.get(link, headers=HEADERS).text
            soup = BeautifulSoup(html, 'html.parser')
            ppl_box = soup.select('div.barr_post > span:nth-of-type(1)')
            if len(ppl_box) == 1:
                # 评论数
                comment = ppl_box[0].get_text()
                # 观看人数
                ppl = soup.select('div.barr_post > span:nth-of-type(3)')[0].get_text()
                # 发布日期
                publishDate = soup.select('div.barr_post > span:nth-of-type(5)')[0].get_text()
                # 搜集该文章的所有文字内容：包括本文和评论
                txt = soup.select('.t_f')
                for w in txt:
                    w = w.get_text()
                    # 逐字检查是否在组内
                    for c in w:
                        # 若该字属于正面组，positive变量加一
                        if c in POSITIVES:
                            positive += 1
                        # 若该字属于负面组，negative变量加一
                        elif c in NEGATIVES: 
                            negative += 1
                data.append((name,comment,ppl,publishDate,positive,negative))
                
                        
            
            # 更新页数
            offset += 1
            url = 'http://8btc.com/forum-2-'+str(offset)+'.html'
    
    # 最后将结果输出到btc.csv文件里
    with open('btc.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        for name, comment, ppl, publishDate, positive, negative in data:
            writer.writerow([name.encode('utf-8'),comment,ppl,publishDate, positive, negative])
    
    
if __name__  == "__main__":
    print("Starting Program")
    main()