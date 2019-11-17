# Python-Crawler
爬虫从零开始
2019-11-17 23:06:24
  response = requests.get(url,headers=header)
  response.encoding = 'utf8'
  print(response.text)
  doc = open('film1.txt','w')
  print(response.text,file=doc)
  doc.close()
 出现错误   UnicodeEncodeError: 'gbk' codec can't encode character '\xa9' in position 205104: illegal multibyte sequence
 改正：   doc = open('film1.txt','w', ,encoding='utf-8')
