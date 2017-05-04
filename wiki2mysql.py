# -*- coding: utf-8 -*-
"""
Created on Thu May  4 21:01:38 2017

@author: zch
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re 
import pymysql.cursors

#请求URL并将结果应UTF-8编码
response = urlopen('https://en.wikipedia.org/wiki/Main_Page').read().decode('utf-8')
#用BeautifulSoup解析
soup = BeautifulSoup(response,'lxml')
#print(soup.head.title.string)
#print(soup)
#p_text = soup.find('a',href=re.compile(r"/wiki/Deaths_in_2017"))
#print(p_text.name,p_text.get_text()) 

#获取所有以/wiki/开头的a标签的href属性
listUrls = soup.find_all('a',href=re.compile('^/wiki/'))
for url in listUrls:
    #过滤掉所有以.jpg或.JPG结尾的url
    if not re.search('\.(jpg|JPG)$',url['href']):
        #输出所有Wikipedia词条和对应的URL链接
        print(url.get_text(),"---->","https://en.wikipedia.org" + url['href'])
        #获取数据库链接
        connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = '123456',
                             db = 'wikiurl',
                             charset = 'utf8mb4')
        try:
            #获取会话指针
            with connection.cursor() as cursor:
                #创建sql语句
                sql = "insert into `urls` (`urlname`,`urlhref`) values (%s,%s)" 
                
                #执行sql语句
                cursor.execute(sql,(url.get_text(),"https://en.wikipedia.org" + url['href']))
                
                #提交
                connection.commit() 
        finally:
            connection.close()
