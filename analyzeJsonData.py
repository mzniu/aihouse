# coding:utf-8
import json
from pymongo import MongoClient
import time
import datetime

today = datetime.date.today()
str_format = '%Y/%m/%d'
uri = 'mongodb://aihouse:passw0rd@127.0.0.1:27017'

def loadTrans():
    f = open("historydata_trans.json")
    setting = json.load(f)
    return setting

def loadVerify():
    f = open("historydata_verify.json")
    setting = json.load(f)
    return setting

def check_record(date):
    client = MongoClient(uri)
    house = client.aihouse
    tran = house.transaction
    try:
        tran.find({'date': str(date)}).next()#2018/3/20存量房网上签约
        print "数据库中已有该日期数据！编号：" + date.encode('utf-8')
        return True
    except:
        print "数据库中未有该日期数据！编号：" + date.encode('utf-8')
        return False
    finally:
        time.sleep(1)
trans=loadTrans()
verify=loadVerify()
print trans
print trans['2018-03-07']
for item in trans:
    result = {}
    date = item.replace("-", "/")
    short_date =date.replace("/0", "/")
    if check_record(date):
        print "Record on "+ str(date) +"is in DB."
    else:
        if item in verify:
            result = {'date': str(date), str(short_date) + '存量房网上签约': {'住宅签约套数：': str(trans[str(item)])},
                      str(item) + '核验房源': {'核验住宅套数：': str(verify[str(item)])}}
        # else:
        #     result = {'date': str(date), str(short_date) + '存量房网上签约': {'住宅签约套数：': str(trans[str(item)])}}
            try:
                client = MongoClient(uri)
                house = client.aihouse
                tran = house.transaction
                tran.insert(result)
            except:
                time.sleep(5)
                client = MongoClient(uri)
                house = client.aihouse
                tran = house.transaction
                tran.insert(result)
    time.sleep(1)
    # date = item.replace("-","/").replace("/0","/")
    # searchStr = str(date)+"存量房网上签约"
    # print searchStr
    # if check_record(date):
    #     print date
    # else:
    #     print date," is not in."
