# coding:utf-8
import datetime
import pymongo
from pymongo import MongoClient

uri = 'mongodb://aihouse:passw0rd@www.mzniu.com:27017'
template_html_path = "webapp/templates/index.html"
static_html_path = "webapp/templates/index_static.html"
recent30_static_html_path = "webapp/templates/recent30_static.html"
recent60_static_html_path = "webapp/templates/recent60_static.html"
recent90_static_html_path = "webapp/templates/recent90_static.html"

app_path = "webapp/app.py"


def gen_index_static_html(template_html_path,static_html_path,date, num_trans, num_verify, weeks, num_week_trans, num_week_verify,date_day30, day30_num_trans):
    template_file = open(template_html_path, "r")
    static_file = open(static_html_path, "w")
    for line in template_file:
        if "{{date}}" in line:
            line = line.replace("{{date}}", str(date))
        elif "{{num_trans}}" in line:
            line = line.replace("{{num_trans}}", str(num_trans))
        elif "{{num_verify}}" in line:
            line = line.replace("{{num_verify}}", str(num_verify))
        elif "{{weeks}}" in line:
            line = line.replace("{{weeks}}", str(weeks))
        elif "{{num_week_trans}}" in line:
            line = line.replace("{{num_week_trans}}", str(num_week_trans))
        elif "{{num_week_verify}}" in line:
            line = line.replace("{{num_week_verify}}", str(num_week_verify))
        elif "{{date_day30}}" in line:
            line = line.replace("{{date_day30}}", str(date_day30))
        elif "{{day30_num_trans}}" in line:
            line = line.replace("{{day30_num_trans}}", str(day30_num_trans))
        static_file.write(line)
    template_file.close()
    static_file.close()


def update_app():
    file_data = ""
    with open(app_path, "r") as f:
        for line in f:
            if "###TEMPLATE-UPDATED:" in line:
                line = "###TEMPLATE-UPDATED:" + str(datetime.datetime.now()) + "\n"
            file_data += line
    with open(app_path, "w") as f:
        f.write(file_data)


def gen_index(days=0,template_html=template_html_path,static_html=static_html_path):
    reverse = -1
    str_format = '%Y/%m/%d'
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    client = MongoClient(uri)
    house = client.aihouse
    trans = house.transaction
    date = []
    date_day30 = []
    num_trans = []
    day30_num_trans = []
    num_verify = []
    weeks = []
    num_week_trans = []
    num_week_verify = []
    count = trans.find().count()
    week_ends = yesterday.strftime(str_format)
    count_week_trans = 0
    count_week_verify = 0
    temp_day30_num = []
    print count
    for item in trans.find().sort("date", pymongo.DESCENDING):
        prefix_date = item['date'].replace("/0", "/").encode("utf-8")
        prefix_date_v = item['date'].replace("/", "-").encode("utf-8")
        dayOfWeek = datetime.datetime.strptime(item['date'], str_format).weekday()
        if dayOfWeek == 6:
            week_ends = prefix_date
            count_week_trans = int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
            count_week_verify = int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
        elif dayOfWeek == 0:
            count_week_trans += int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
            count_week_verify += int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
            num_week_trans.append(count_week_trans)
            num_week_verify.append(count_week_verify)
            weeks.append(prefix_date + "-" + week_ends)
        else:
            count_week_trans += int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
            count_week_verify += int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
        temp_day30_num.append(int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8")))
        if len(temp_day30_num) == 30:
            day30_num_trans.append(sum(temp_day30_num) / len(temp_day30_num))
            temp_day30_num = temp_day30_num[1:]
        date.append(prefix_date)
        num_trans.append(int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8")))
        num_verify.append(int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8")))
    if days == 0:
        reverse = -1
        count_week = 0
        date_day30 = date[:-30]
        days = count
    else:
        reverse = 1
        count_week = int((days+6)/7)
        date_day30 = date[:]
    #print date_day30[days::-1]
    gen_index_static_html(template_html,static_html,date=date[days::-1], num_trans=num_trans[days::-1], num_verify=num_verify[days::-1],
                                 weeks=weeks[count_week::-1], num_week_trans=num_week_trans[count_week::-1],
                                 num_week_verify=num_week_verify[count_week::-1],date_day30=date_day30[days::-1], day30_num_trans=day30_num_trans[days::-1])


gen_index()
gen_index(days=30,template_html=template_html_path,static_html=recent30_static_html_path)
gen_index(days=60,template_html=template_html_path,static_html=recent60_static_html_path)
gen_index(days=90,template_html=template_html_path,static_html=recent90_static_html_path)
update_app()
