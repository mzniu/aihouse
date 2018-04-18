# coding:utf-8
import datetime
import pymongo
from pymongo import MongoClient

uri = 'mongodb://aihouse:passw0rd@www.mzniu.com:27017'
template_html_path = "webapp/templates/index.html"
lianjia_html_path = "webapp/templates/lianjia_template.html"
lianjia_area_html_path = "webapp/templates/lianjia_area_template.html"
static_html_path = "webapp/templates/index_static.html"
recent30_static_html_path = "webapp/templates/recent30_static.html"
recent120_static_html_path = "webapp/templates/recent120_static.html"
recent360_static_html_path = "webapp/templates/recent360_static.html"
lianjia_static_html_path = "webapp/templates/lianjia_static.html"
lianjia_area_static_html_path = "webapp/templates/lianjia_area_static.html"

app_path = "webapp/app.py"


def gen_index_static_html(template_html_path, static_html_path, date, num_trans, num_verify, weeks, num_week_trans,
                          num_week_verify, date_day30, day30_num_trans):
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


def gen_lianjia_static_html(lianjia_html_path, static_html_path, date, num_total_trans, num_new_publish,
                            num_new_takelook, num_new_buyer, num_on_sale, num_recent90_trans):
    template_file = open(lianjia_html_path, "r")
    static_file = open(static_html_path, "w")
    for line in template_file:
        if "{{date}}" in line:
            line = line.replace("{{date}}", str(date))
        elif "{{num_total_trans}}" in line:
            line = line.replace("{{num_total_trans}}", str(num_total_trans))
        elif "{{num_new_publish}}" in line:
            line = line.replace("{{num_new_publish}}", str(num_new_publish))
        elif "{{num_new_takelook}}" in line:
            line = line.replace("{{num_new_takelook}}", str(num_new_takelook))
        elif "{{num_new_buyer}}" in line:
            line = line.replace("{{num_new_buyer}}", str(num_new_buyer))
        elif "{{num_on_sale}}" in line:
            line = line.replace("{{num_on_sale}}", str(num_on_sale))
        elif "{{num_recent90_trans}}" in line:
            line = line.replace("{{num_recent90_trans}}", str(num_recent90_trans))
        static_file.write(line)
    template_file.close()
    static_file.close()


def gen_lianjia_area_static_html(html_path, static_html_path, date, num_new_trans,
                            num_new_takelook, num_on_sale, num_recent90_trans):
    template_file = open(html_path, "r")
    static_file = open(static_html_path, "w")
    for line in template_file:
        if "{{date}}" in line:
            line = line.replace("{{date}}", str(date))
        elif "{{num_new_trans}}" in line:
            line = line.replace("{{num_new_trans}}", str(num_new_trans))
        elif "{{num_new_takelook}}" in line:
            line = line.replace("{{num_new_takelook}}", str(num_new_takelook))
        elif "{{num_on_sale}}" in line:
            line = line.replace("{{num_on_sale}}", str(num_on_sale))
        elif "{{num_recent90_trans}}" in line:
            line = line.replace("{{num_recent90_trans}}", str(num_recent90_trans))
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


def gen_index(days=0, template_html=template_html_path, static_html=static_html_path):
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
        date_day30 = date[:-30]
        days = count
        count_week = int((days + 6) / 7)
    else:
        reverse = 1
        count_week = int((days + 6) / 7)
        date_day30 = date[:]
    # print date_day30[days::-1]
    gen_index_static_html(template_html, static_html, date=date[days::-1], num_trans=num_trans[days::-1],
                          num_verify=num_verify[days::-1],
                          weeks=weeks[count_week::-1], num_week_trans=num_week_trans[count_week::-1],
                          num_week_verify=num_week_verify[count_week::-1], date_day30=date_day30[days::-1],
                          day30_num_trans=day30_num_trans[days::-1])


def gen_lianjia(days=0, template_html=template_html_path, static_html=static_html_path):
    reverse = -1
    str_format = '%Y/%m/%d'
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    client = MongoClient(uri)
    house = client.aihouse
    lianjia = house.lianjia_statistics
    date = []
    date_day30 = []
    num_total_trans = []
    day30_num_trans = []
    num_new_publish = []
    num_new_takelook = []
    num_new_buyer = []
    num_on_sale = []
    num_recent90_trans = []
    weeks = []
    num_week_trans = []
    num_week_verify = []
    count = lianjia.find().count()
    week_ends = yesterday.strftime(str_format)
    count_week_trans = 0
    count_week_verify = 0
    temp_day30_num = []
    print count
    for item in lianjia.find().sort("date", pymongo.DESCENDING):
        prefix_date = item['date'].replace("/0", "/").encode("utf-8")
        prefix_date_v = item['date'].replace("/", "-").encode("utf-8")
        # dayOfWeek = datetime.datetime.strptime(item['date'], str_format).weekday()
        # if dayOfWeek == 6:
        #     week_ends = prefix_date
        #     count_week_trans = int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        #     count_week_verify = int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
        # elif dayOfWeek == 0:
        #     count_week_trans += int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        #     count_week_verify += int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
        #     num_week_trans.append(count_week_trans)
        #     num_week_verify.append(count_week_verify)
        #     weeks.append(prefix_date + "-" + week_ends)
        # else:
        #     count_week_trans += int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        #     count_week_verify += int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
        # temp_day30_num.append(int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8")))
        # if len(temp_day30_num) == 30:
        #     day30_num_trans.append(sum(temp_day30_num) / len(temp_day30_num))
        #     temp_day30_num = temp_day30_num[1:]
        date.append(prefix_date)
        num_total_trans.append(int(item['total_trans']))
        num_new_publish.append(int(item['new_publish'].encode("utf-8")))
        num_new_takelook.append(int(item['new_takelook'].encode("utf-8")))
        num_new_buyer.append(int(item['new_buyer'].encode("utf-8")))
        num_on_sale.append(int(item['on_sale'].encode("utf-8")))
        num_recent90_trans.append(int(item['recent90_trans'].encode("utf-8")))
    if days == 0:
        reverse = -1
        date_day30 = date[:-30]
        days = count
        count_week = int((days + 6) / 7)
    else:
        reverse = 1
        count_week = int((days + 6) / 7)
        date_day30 = date[:]
    # print date
    # print num_total_trans
    gen_lianjia_static_html(template_html, static_html, date=date[days::-1], num_total_trans=num_total_trans[days::-1],
                            num_new_publish=num_new_publish[days::-1], num_new_takelook=num_new_takelook[days::-1],
                            num_new_buyer=num_new_buyer[days::-1], num_on_sale=num_on_sale[days::-1],
                            num_recent90_trans=num_recent90_trans[days::-1])


def gen_lianjia_area(days=0, template_html=lianjia_area_html_path, static_html=lianjia_area_static_html_path):
    reverse = -1
    str_format = '%Y/%m/%d'
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    client = MongoClient(uri)
    house = client.aihouse
    lianjia = house.lianjia_statistics
    date = []
    date_day30 = []
    num_new_trans = []
    day30_num_trans = []
    num_new_publish = []
    num_new_takelook = []
    num_new_buyer = []
    num_on_sale = []
    num_recent90_trans = []
    weeks = []
    num_week_trans = []
    num_week_verify = []
    count = lianjia.find().count()
    week_ends = yesterday.strftime(str_format)
    count_week_trans = 0
    count_week_verify = 0
    temp_day30_num = []
    print count
    for item in lianjia.find().sort("date", pymongo.DESCENDING):
        prefix_date = item['date'].replace("/0", "/").encode("utf-8")
        prefix_date_v = item['date'].replace("/", "-").encode("utf-8")
        # dayOfWeek = datetime.datetime.strptime(item['date'], str_format).weekday()
        # if dayOfWeek == 6:
        #     week_ends = prefix_date
        #     count_week_trans = int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        #     count_week_verify = int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
        # elif dayOfWeek == 0:
        #     count_week_trans += int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        #     count_week_verify += int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
        #     num_week_trans.append(count_week_trans)
        #     num_week_verify.append(count_week_verify)
        #     weeks.append(prefix_date + "-" + week_ends)
        # else:
        #     count_week_trans += int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8"))
        #     count_week_verify += int(item[prefix_date_v + u'核验房源'][u'核验住宅套数：'].encode("utf-8"))
        # temp_day30_num.append(int(item[prefix_date + u'存量房网上签约'][u'住宅签约套数：'].encode("utf-8")))
        # if len(temp_day30_num) == 30:
        #     day30_num_trans.append(sum(temp_day30_num) / len(temp_day30_num))
        #     temp_day30_num = temp_day30_num[1:]
        date.append(prefix_date)
        num_new_trans.append(int(item['tongzhou']['new_trans'].encode("utf-8")))
        num_new_takelook.append(int(item['tongzhou']['new_takelook'].encode("utf-8")))
        num_on_sale.append(int(item['tongzhou']['on_sale'].encode("utf-8")))
        num_recent90_trans.append(int(item['tongzhou']['recent90_trans'].encode("utf-8")))
    if days == 0:
        reverse = -1
        date_day30 = date[:-30]
        days = count
        count_week = int((days + 6) / 7)
    else:
        reverse = 1
        count_week = int((days + 6) / 7)
        date_day30 = date[:]
    # print date
    # print num_total_trans
    gen_lianjia_area_static_html(template_html, static_html, date=date[days::-1], num_new_trans=num_new_trans[days::-1],
                             num_new_takelook=num_new_takelook[days::-1], num_on_sale=num_on_sale[days::-1],
                            num_recent90_trans=num_recent90_trans[days::-1])

# gen_index()
# gen_index(days=30, template_html=template_html_path, static_html=recent30_static_html_path)
# gen_index(days=120, template_html=template_html_path, static_html=recent120_static_html_path)
# gen_index(days=360, template_html=template_html_path, static_html=recent360_static_html_path)
# gen_lianjia(days=0, template_html=lianjia_html_path, static_html=lianjia_static_html_path)
gen_lianjia_area(days=0, template_html=lianjia_area_html_path, static_html=lianjia_area_static_html_path)
update_app()
