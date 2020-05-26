# encoding=utf8
import sys
#import urllib2
from bs4 import BeautifulSoup
import execjs
import re
import requests
import csv

# 用于HTTP的GET请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36'
}

# 正面的情绪字
POSITIVES = ['好','涨','牛','红','赚']

# 负面的情绪字
NEGATIVES = ['差','跌','熊','绿','亏']

# 導出的csv欄位名
TARGETS = ['文章名称','评论数','阅览数','发布日期','正面字','负面字']


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
    first_html = req.content.decode('utf-8')
    print(first_html)
    # 执行JS获取Cookie
    cookie_str = executejs(first_html)
    # 将Cookie转换为字典格式
    cookie = parse_cookie(cookie_str)
    cookie_id = req.cookies
    cookie_id = '; '.join(['='.join(item) for item in cookie_id.items()])
    return (cookie_id, cookie.keys()[0]+"="+cookie.values()[0])


def main():
    #reload(sys)#python2 needs explicit encoding definition
    #sys.setdefaultencoding('utf8')
    # 定义变量
    data =[] # 储存结果的容器
    offset = 1 # 记录论坛的当前页数
    bound = input("Number of pages to crawl: ")
    bound = int(bound)
    
    
    """ ----- Uncomment this if http gives error 502
    # 从第一次普通访问截取cookie
    cookies = getCookie(url)
    setCookie = cookies[0]+';'+cookies[1]
    # 将截取到的两个cookies加入到以后请求的头里
    HEADERS.update({'Cookie':setCookie})    
     -----"""

    
    #循环到使用者设定的页数
    while offset < bound+1:
        print("On page {}".format(offset))
        url = 'https://www.chainnode.com/forum-2-'+str(offset)+'.html'
        html=requests.get(url,headers=HEADERS).text
        #print(html)
        soup = BeautifulSoup(html, 'html.parser')

        post_divs = soup.find_all('a',attrs={'class':'bbt-block'})

        for div in post_divs:
            #div.prettify('gb18030')
            #div.encode('gb18030')
            positive = 0
            negative = 0
            # 文章名称
            name = div.get_text().strip()
            # 获取文章链接
            link = "https://www.chainnode.com"+div.get('href')
            print(link)
            # 进入文章链接
            html = requests.get(link, headers=HEADERS).text
            soup = BeautifulSoup(html, 'html.parser')
            ppl_box = soup.select('div.header-module__num')
            if len(ppl_box) == 1:
                # 评论数
                comment = soup.select('div.header-module__num > span:nth-of-type(2)')[0].get_text()
                # 观看人数
                ppl = soup.select('div.header-module__num > span:nth-of-type(1)')[0].get_text()
                # 发布日期
                publishDate = soup.select('time')[0].get_text()
                
                # Collect words from the content
                paragraphs = soup.select('p')

                for p in paragraphs:
                    
                    txt = p.get_text()
                    
                    for w in txt:
                        # If the character belongs to the positive set
                        if w in POSITIVES:
                            positive += 1
                        # If the character belongs to the negative set
                        elif w in NEGATIVES: 
                            negative += 1
                data.append((name,comment,ppl,publishDate,positive,negative))             
        # Update page number
        offset +=1
        print(url)
        
    
    # Output data into file 'btc.csv'
    with open('btc.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(TARGETS)
        for name, comment, ppl, publishDate, positive, negative in data:
            writer.writerow([name, comment, ppl, publishDate, positive, negative])
    
    
if __name__  == "__main__":
    print("Starting Program")
    main()