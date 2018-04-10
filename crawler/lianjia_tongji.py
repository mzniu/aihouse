# coding:utf-8
import requests
import re
import datetime
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient

str_format = '%Y/%m/%d'
uri = 'mongodb://mzniu:Nmz53187223@www.mzniu.com:27017'
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tongji_url = 'https://bj.lianjia.com/fangjia/'
list_url = 'http://210.75.213.188/shh/portal/bjjs2016/list.aspx?pagenumber='
detailed_url = 'http://210.75.213.188/shh/portal/bjjs2016/'


def get_record():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    print "当前需要添加日期："+str(yesterday.strftime(str_format))
    response = requests.get(tongji_url)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        source = response.text
    else:
        print response.status_code
    soup = BeautifulSoup(response.text, "html.parser")
    if soup is not None:
        today_lianjia = soup.find('div', class_="item item-1-3").find_all('span')[0].text.split(u"日")[0]
        today_lianjia = str(today_lianjia.replace(u"月", "/"))
        if check_record():
            pass
        else:
            if str(yesterday.strftime(str_format)).endswith(today_lianjia):
                print today_lianjia
                lianjia_average_title = soup.find('div', class_="qushi-1").find('span').text
                lianjia_average_num = soup.find('div', class_="qushi-2").find('span').text
                new_publish = soup.find_all('div', class_="item item-1-3")[0].find_all('span')[2].text
                new_buyer = soup.find_all('div', class_="item item-1-3")[1].find('div', class_="num").find('span').text
                new_takelook = soup.find_all('div', class_="item item-1-3")[2].find('div', class_="num").find('span').text
                on_sale = \
                    soup.find('div', class_="qushi-2").find_all('a', class_="txt")[0].text.split(u"房源")[1].split(u"套")[0]
                recent90_trans = \
                soup.find('div', class_="qushi-2").find_all('a', class_="txt")[1].text.split(u"房源")[1].split(u"套")[0]
                result = {"update_date": str(datetime.datetime.today()),"date":str(yesterday.strftime(str_format)),
                          lianjia_average_title:lianjia_average_num,"new_publish":new_publish,"new_buyer":new_buyer,
                          "new_takelook":new_takelook,"on_sale":on_sale,"recent90_trans":recent90_trans}
                print lianjia_average_num,new_publish, new_buyer, new_takelook, on_sale, recent90_trans
                print "添加新数据到数据库！"
                try:
                    client = MongoClient(uri)
                    house = client.aihouse
                    stat = house.lianjia_statistics
                    stat.insert(result)
                except:
                    time.sleep(5)
                    client = MongoClient(uri)
                    house = client.aihouse
                    stat = house.lianjia_statistics
                    stat.insert(result)


def check_record():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    client = MongoClient(uri)
    house = client.aihouse
    stat = house.lianjia_statistics
    try:
        stat.find({'date': yesterday.strftime(str_format)}).next()
        print "数据库中已有当前日期数据！"
        return True
    except:
        print "数据库中未有当前日期数据！"
        return False


get_record()

