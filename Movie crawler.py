import requests
import re
import sys
# from time import time   不要快速访问
# reload(sys) python3中已无此函数
# sys.setdefaultencoding('utf8') python3默认编码utf8
#确认访问地址
url = 'http://www.1905.com/mtalk/?fr=homepc_menu_cmt'
#确认查找规则-正则表达式 pattern：规则 herf:超链接
pattern = '<figcaption class="list-title"><a href="(.*?)" target="_blank">(.*?)</a></figcaption>'
# < figcaption class ="list-title" > < a href="https://www.1905.com/video/play/1412885.shtml" target="_blank" > 同台竞技的《我和我的祖国》：7位导演各有千秋胜负难论 < / a > < / figcaption >
#(.*?)取     .*?不加括号，我什么都不取
#加一个请求头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'    #IE浏览器F12-网络调出
}
#请求地址
response = requests.get(url,headers=header) #header要求字典形式
#注意编码按照页面编码制定，源码头部标出了
response.encoding = 'utf8'

print(response)
# print(response.text)

#匹配我要的东西，如果没有flags=re.S，换行就不找了
result = re.findall(string=response.text,pattern=pattern,flags=re.S)
# print(result)
# for i in result:
#     for j in i:
#         print(j)
# file = "D:\date\film.txt"
for i in result:
    print(i[0],i[1])            #a 追加,as:引用
    with open('film.txt', 'a')as w:
        w.write(i[1]+i[0]+'\n')
# D:\date\winequality\sample_accident.csv

a = (('new1','link1'),('new2','link2'))
for i in a:
    for j in i:
        print(j)
for i in a:
     print (i[0], i[1]) #以后操作数据库用
