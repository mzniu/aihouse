# coding:utf-8
import requests, json
import datetime, time
from bs4 import BeautifulSoup
from pymongo import MongoClient

str_format = '%Y/%m/%d'
uri = 'mongodb://mzniu:Nmz53187223@www.mzniu.com:27017'
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
request_url = 'http://www.bjjs.gov.cn/bjjs/fwgl/fdcjy/fwjy/index.shtml'
request_url2 = 'http://210.75.213.188/shh/portal/bjjs/index.aspx'

def get_record():
    print "当前需要抓取日期为：" + str(yesterday)
    response = requests.get(request_url)
    response2 = requests.get(request_url2)
    response.encoding = response.apparent_encoding
    response2.encoding = response.apparent_encoding
    if response.status_code == 200:
        source = response.text
    else:
        print response.status_code
    if response2.status_code == 200:
        source2 = response2.text
    else:
        print response2.status_code

    soup = BeautifulSoup(response.text, "html.parser")
    soup2 = BeautifulSoup(response2.text, "html.parser")
    result = {'date': yesterday.strftime(str_format), "source": source, "sourc2": source2}
    for table in soup.find_all('div', class_="portlet")[0].find_all('table')[1].find_all('table'):
        table_data = [[cell.text for cell in row("td")]
                      for row in table("tr")]
        for index in range(len(table_data)):
            if len(table_data[index]) < 2:
                if str.strip(table_data[index][0].encode('utf-8')) == "":
                    table_data.remove(table_data[index])
                elif str.strip(table_data[index][0].encode('utf-8')).startswith("截止日期"):
                    table_data[index] = str.strip(table_data[index][0].encode('utf-8')).split("：")
                    deu_date = datetime.datetime.strptime(table_data[index][1], str_format)
                    print "当前网站截止日期为：" + str(deu_date.date())
                else:
                    table_data[index].append("")
            else:
                table_data[index][0] = str.strip(table_data[index][0].encode('utf-8'))
                table_data[index][1] = str.strip(table_data[index][1].encode('utf-8'))
        result = dict(result, **{table_data[0][0]: json.loads(json.dumps(dict(table_data[1:])))})

    for table in soup.find_all('div', class_="portlet")[1].find_all('table')[1].find_all('table'):
        table_data = [[cell.text for cell in row("td")]
                      for row in table("tr")]
        for index in range(len(table_data)):
            if len(table_data[index]) < 2:
                if table_data[index][0] == "":
                    table_data[index].remove(table_data[index][0])
                table_data[index][0] = str.strip(table_data[index][0].encode('utf-8'))
            else:
                table_data[index][0] = str.strip(table_data[index][0].encode('utf-8'))
                table_data[index][1] = str.strip(table_data[index][1].encode('utf-8'))
        result = dict(result, **{table_data[0][0]: json.loads(json.dumps(dict(table_data[1:])))})

    table_data2 = []
    for table in soup2.find_all('table', class_="tjInfo")[0].find_all("tr"):
        # print table.find("td")
        if table.find("td") is not None:
            table_data2.append([table.find("th").text, table.find("td").text])
        else:
            table_data2.append([table.find("th").text])
    result = dict(result, **{table_data2[0][0]: json.loads(json.dumps(dict(table_data2[1:])))})

    if deu_date.date() == yesterday and check_record() is not True:
        print "添加新数据到数据库！"
        client = MongoClient(uri)
        house = client.aihouse
        tran = house.transaction
        tran.insert(result)
    else:
        print "数据未更新!"


def check_record():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    client = MongoClient(uri)
    house = client.aihouse
    tran = house.transaction
    try:
        tran.find({'date': yesterday.strftime(str_format)}).next()
        print "数据库中已有当前日期数据！"
        return True
    except:
        print "数据库中未有当前日期数据！"
        return False

# get_record()
count = 1
while True:
    print "======================================"
    print "总计第" + str(count) + "次抓取" + " 当前时间： " + str(datetime.datetime.today())
    get_record()
    time.sleep(3600)
    count += 1
