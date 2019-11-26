import requests
import re
import json
import time
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
from lxml import etree

# 获取页面源码
def get_one_page(url):
    try:
        headers = {  # 伪装请求头
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        response = requests.get(url, headers=headers)  # 构造响应

        if response.status_code == 200:  # 判断状态码
            return response.text
        return None
    except requests.exceptions.RequestException as r:
        return None

# 正则表达式提取源码关键信息
def parse_one_page(html):
    # 正则表达式查询目标信息
    pattern = re.compile(
        '<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        # 包含yield表达式的函数是特殊的函数，叫做生成器函数(generator function)，被调用时将返回一个迭代器（iterator），调用时可以使用next或send(msg)。它的用法与return相似，区别在于它会记住上次迭代的状态，继续执行。
        yield{  # yield关键字
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3].strip()[3:],  # if len(item[3])>3 else '',
            'time': item[4].strip()[5:],  # if len(item[4])>5 else '',
            'score': item[5].strip()+item[6].strip()
        }

#Xpath提取信息
def xpath_demo(html):
    html=etree.HTML(html)
    str1='//dd['
    for i in range(10):
        yield{  # yield关键字
            'index': html.xpath(str1+str(i)+']/i/text()'),
            'image': html.xpath(str1+str(i)+']/a/img[@class="board-img"]/@data-src'),
            'title': html.xpath(str1+str(i)+']//p/a[@data-act="boarditem-click"]/text()'),
            'actor': ''.join(html.xpath(str1+str(i)+']//p[@class="star"]/text()')).strip(),
            'time': html.xpath(str1+str(i)+']//p[@class="releasetime"]/text()'),
            'score': ''.join(html.xpath(str1+str(i)+']//p[@class="score"]/i/text()')),
        }

# bs4提取关键信息
def bs4_demo(html):
    soup = BeautifulSoup(html, 'lxml')
    # pq=PyQuery(html)
    # for item in pq('dd img/.board-img')
    for dd in soup.find_all(name='dd'):
        yield{
            'index': dd.find(name='i', attrs={'class': 'board-index'}).string.strip(),#去掉前后空格
            'image': dd.find(name='img', attrs={'class': 'board-img'})['data-src'],
            'title': dd.find(name='p', attrs={'class': 'name'}).string.strip(),
            'actor': dd.find(name='p', attrs={'class': 'star'}).string.strip(),
            'time': dd.find(name='p', attrs={'class': 'releasetime'}).string.strip(),
            'score': dd.find(name='i', attrs={'class': 'integer'}).string+dd.find(name='i', attrs={'class': 'fraction'}).string
        }

#pyquery css筛选信息
def pyquery_demo(html):
    doc=pq(html)
    for dd in doc('dd').items():
        yield{
            'index': dd.find('i.board-index').text(),#获取文本
            'image': dd.find('img.board-img').attr('data-src'),#获取属性
            'title': dd.find('p.name a').text(),
            'actor': dd.find('p.star').text(),
            'time': dd.find('p.releasetime').text(),
            'score': dd.find('p.score i.integer').text()+dd.find('p.score i.fraction').text()
        }

def write_to_file(content):
    with open('/Users/zz/Desktop/result.txt', 'a', encoding='utf-8') as f:
        # json.dumps()实现字典的序列化，ensure_ascii=False保证输出非Unicode编码
        f.write(json.dumps(content, ensure_ascii=False)+'/n')


def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    # for item in parse_one_page(html):
    #for item in bs4_demo(html):
    #for item in pyquery_demo(html):
    for item in xpath_demo(html):
        print(item)
        # write_to_file(item)  # 写入文件


if __name__ == '__main__':  # 是否从控制台执行
    for i in range(10):
        main(offset=i*10)
        time.sleep(1)#避免操作过快被识别
