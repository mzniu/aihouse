# coding:utf-8
import datetime
import pymongo
from pymongo import MongoClient

uri = 'mongodb://aihouse:passw0rd@127.0.0.1:27017'
template_html_path = "webapp/templates/index.html"
static_html_path = "webapp/templates/index_static.html"


def gen_index_static_html(date, num_trans, num_verify, weeks, num_week):
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
        elif "{{num_week}}" in line:
            line = line.replace("{{num_week}}", str(num_week))
        static_file.write(line)
    template_file.close()
    static_file.close()

def gen_index():
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
            count_week_trans += int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
            num_week.append(count_week_trans)
            weeks.append(prefix_date + "-" + week_ends)
        else:
            count_week_trans += int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        date.append(prefix_date)
        num_trans.append(int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8")))
        num_verify.append(int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8")))
    return gen_index_static_html(date=date[::-1], num_trans=num_trans[::-1], num_verify=num_verify[::-1],
                           weeks=weeks[::-1], num_week=num_week[::-1])


gen_index()
