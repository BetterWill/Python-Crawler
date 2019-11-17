import requests
import re
import sys


url = 'https://search.suning.com/耐克/'
# pattern = '<figcaption class="list-title"><a href="(.*?)" target="_blank">(.*?)</a></figcaption>'
pattern = 'name="ssdsn_search_pro_name.*?0000000000" title="苏宁体育自营 品质服务保证"target="_blank" href="(.*?)"><b class="highlight">(.*?)<em  style="display:none" >'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'    #IE浏览器F12-网络调出
}
response = requests.get(url,headers=header)
response.encoding = 'utf8'
# print(response.text)
# doc = open('film1.txt','w', encoding='utf-8')
# print(response.text,file=doc)
# doc.close()
result = re.findall(string=response.text,pattern=pattern,flags=re.S)
for i in result:
    print(i[0], i[1])            #a 追加,as:引用
    with open('filmSuning.txt', 'a')as w:
        w.write(i[0]+i[1]+'\n')

