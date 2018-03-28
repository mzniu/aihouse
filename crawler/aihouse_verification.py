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
request_url = 'http://210.75.213.188/shh/portal/bjjs2016/list.aspx?pagenumber=1'
list_url = 'http://210.75.213.188/shh/portal/bjjs2016/list.aspx?pagenumber='
detailed_url = 'http://210.75.213.188/shh/portal/bjjs2016/'


def get_record(page):

    response = requests.get(list_url + str(page))
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        source = response.text
    else:
        print response.status_code
    print("获取第" + str(page) + "页数据：StatusCode["+str(response.status_code)+"]")
    soup = BeautifulSoup(response.text, "html.parser")
    if soup is not None:
        head = soup.find('table', class_="houseList").find('thead').find_all('th')
        for tr in soup.find('table', class_="houseList").find('tbody').find_all('tr'):
            td = tr.find_all('td')
            if check_record(td[0].text):
                pass
            else:
                result = {"update_date": str(datetime.datetime.today())}
                for index in range(len(head)):
                    if index == len(head) - 1:
                        result = dict(result, **{head[index].text: td[index].a['href']})
                    else:
                        result = dict(result, **{head[index].text: td[index].text})
                print "添加新数据到数据库！"
                try:
                    client = MongoClient(uri)
                    house = client.aihouse
                    verify = house.verification
                    verify.insert(result)
                except:
                    time.sleep(5)
                    client = MongoClient(uri)
                    house = client.aihouse
                    verify = house.verification
                    verify.insert(result)
            time.sleep(1)
        else:
            print "Soup returns None!"
        # table_data = [[cell.text for cell in row("td")]
        #               for row in table("tr")]
        # for index in range(len(table_data)):
        #     if len(table_data[index]) < 2:
        #         if str.strip(table_data[index][0].encode('utf-8')) == "":
        #             table_data.remove(table_data[index])
        #         elif str.strip(table_data[index][0].encode('utf-8')).startswith("截止日期"):
        #             table_data[index] = str.strip(table_data[index][0].encode('utf-8')).split("：")
        #             deu_date = datetime.datetime.strptime(table_data[index][1], str_format)
        #             print "当前网站截止日期为：" + str(deu_date.date())
        #         else:
        #             table_data[index].append("")
        #     else:
        #         table_data[index][0] = str.strip(table_data[index][0].encode('utf-8'))
        #         table_data[index][1] = str.strip(table_data[index][1].encode('utf-8'))
        # result = dict(result, **{table_data[0][0]: json.loads(json.dumps(dict(table_data[1:])))})


def get_pagenum():
    response = requests.get(request_url)
    response.encoding = response.apparent_encoding
    if response.status_code == 200:
        source = response.text
    else:
        print response.status_code

    soup = BeautifulSoup(response.text, "html.parser")

    page_table = re.findall(r"\d+", soup.find_all('div')[-1].find_all('td')[0].text)
    if page_table is not None:
        return int(page_table[0]) / 7
    # for tr in soup.find('table', class_="houseList").find('tbody').find_all('tr'):


def check_record(verify_id):
    client = MongoClient(uri)
    house = client.aihouse
    verify = house.verification
    try:
        verify.find({'核验编号': verify_id}).next()
        print "数据库中已有核验编号数据！编号：" + verify_id.encode('utf-8')
        return True
    except:
        print "数据库中未有核验编号数据！编号：" + verify_id.encode('utf-8')
        return False
    finally:
        time.sleep(1)


def check_record_inpage(start_page, end_page, orginal_page):
    print("检查第" + str(start_page) + "页数据：")
    if start_page == end_page:
        print "返回所需页面："+str(start_page)
        get_record(start_page)
        time.sleep(20)
    elif start_page > end_page:
        response = requests.get(list_url + str(start_page))
        response.encoding = response.apparent_encoding
        if response.status_code == 200:
            source = response.text
        else:
            print response.status_code

        soup = BeautifulSoup(response.text, "html.parser")
        for tr in soup.find('table', class_="houseList").find('tbody').find_all('tr'):
            td = tr.find_all('td')
            if check_record(td[0].text):
                pass
            else:
                print "该页面有未添加数据记录：", orginal_page, start_page, orginal_page
                check_record_inpage(orginal_page, start_page, orginal_page)
                break
            # time.sleep(1)
        print "该页面没有未添加数据记录：", (start_page + end_page) / 2, end_page, start_page - 1
        check_record_inpage((start_page + end_page) / 2, end_page, start_page-1)


# get_record(2)
total_page = get_pagenum()
print check_record_inpage(total_page, 0, total_page)
# for i in range(get_pagenum() + 1, 1, -1):
#     temp = 0
#     while check_record_inpage(i):
#         temp =
#     get_record(i)
#     time.sleep(20)
