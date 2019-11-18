# coding:utf-8
#python  V3.7
import requests
import sqlite3
import json
import random       #防止照片重名

#建立一个函数find()
def find():
    #确认访问地址
    url2 = 'https://www.1905.com/api/content/index.php'#消息头的请求网址
    # 加一个请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    }
    # 确定请求参数
    parmas = {
        'callback': 'reloadList',
        'm': 'converged',
        'a': 'info',
        'type': 'jryp',
        'year': '2019',
        'month': '8',
    }
    #请求地址
    response = requests.get(url2,headers=header,params=parmas)
    #由于返回的是有元组 所以要去一些内容
    result = response.text          #此时不是字典，需要变为字典
    #json字符串转字典格式  //json.dumps 字典格式转json字符串 下面步骤为去掉reloadlist元组
    result = result.replace( 'reloadList(' , '').replace(')','')
    # 从json格式读取，json.dumps 字典格式转json字符串，json.loads(result)是反方向的
    result = json.loads(result)

    for i in result['info']:
        print(i['url'], i['title'], i['thumb'])
        img = requests.get(i['thumb']).content
        #保存图片 保存用wb write bytes 二进制
        img_name = random.randint(10000, 99999)
        with open('img%s.jpg'%img_name, 'wb') as w:  #wb二进制
            w.write(img)
        createDB()
        save_data(content=i['title'],link=i['url'], img=img_name)


#创建数据库
def createDB():
    conn = sqlite3.connect('film.db')
    c= conn.cursor()            #cursor游标,增删改的民工
    c.execute('CREATE TABLE filmdata(id INTEGER PRIMARY KEY AUTOINCREMENT, content text, link text, img text)')
    conn.commit()  #干
    conn.close()

#存储爬虫的数据
def save_data(content, link, img):
    conn = sqlite3.connect('film.db')
    c = conn.cursor()                   #双引号里面就不能在混用双引号了{0}占位符
    c.execute("INSERT into filmdata(content, link, img)VALUES('{0}','{1}','{2}')".format(content, link, img))
    conn.commit()
    conn.close()

#查看数据库内容
def showdata():
    conn = sqlite3.connect('film.db')
    c = conn.cursor()
    res = c.execute('SELECT * from filmdata')
    print (res)
    for i in res:
        print (i[1])
    conn.close()

if __name__ =='__main__':
    # createDB()
    # find()
    showdata()








