# coding:utf-8
###TEMPLATE-UPDATED:2018-04-07 23:00:59.924000
from flask import Flask, render_template
# from flask.ext.bootstrap import Bootstrap #专为Flask开发发拓展都暴露在flask.ext命名空间下，Flask-Bootstrap输出一个Bootstrap类
from flask_bootstrap import Bootstrap
import pymongo
from pymongo import MongoClient
import json
import ast
import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)  # Flask扩展一般都在创建实例时初始化，这行代码是Flask-Bootstrap的初始化方法
uri = 'mongodb://aihouse:passw0rd@127.0.0.1:27017'


@app.route('/')
def index():
    return render_template('index_static.html')

@app.route('/recent30')
def recent30():
    return render_template('recent30_static.html')


@app.route('/recent60')
def recent60():
    return render_template('recent60_static.html')\

@app.route('/recent90')
def recent90():
    return render_template('recent90_static.html')


@app.route('/trans')
def trans():
    str_format = '%Y/%m/%d'
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    client = MongoClient(uri)
    house = client.aihouse
    trans = house.transaction
    date = []
    num_trans = []
    num_all = []
    num_verify = []
    weeks = []
    num_week = []
    print trans.find().count()
    week_ends = yesterday.strftime(str_format)
    count_week_trans = 0
    for item in trans.find().sort("date", pymongo.DESCENDING):
        prefix_date = item['date'].replace("/0", "/").encode("utf-8")
        prefix_date_v = item['date'].replace("/", "-").encode("utf-8")
        dayOfWeek = datetime.datetime.strptime(item['date'], str_format).weekday()
        if dayOfWeek == 6:
            week_ends = prefix_date
            count_week_trans = int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        elif dayOfWeek == 0:
            count_week_trans+= int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
            num_week.append(count_week_trans)
            weeks.append(prefix_date+"-"+week_ends)
        else:
            count_week_trans+= int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        date.append(prefix_date)
        num_trans.append(int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8")))
        num_verify.append(int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8")))
    return render_template('trans.html', date=date[::-1], num_trans=num_trans[::-1], num_verify=num_verify[::-1], weeks=weeks[::-1], num_week=num_week[::-1])


@app.route('/verify')
def verify():
    client = MongoClient(uri)
    house = client.aihouse
    trans = house.transaction
    date = []
    num = []
    num_all = []
    print trans.find().count()
    for item in trans.find().sort("date", pymongo.DESCENDING):
        prefix_date = item['date'].replace("/0", "/").encode("utf-8")
        date.append(prefix_date)
        num.append(int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8")))
        num_all.append(int(item[prefix_date + u'存量房网上签约'][u'网上签约套数：'].encode("utf-8")))
        print date
    return render_template('verify.html', date=date, num=num, num_all=num_all)


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 81,debug=True, threaded = True)
