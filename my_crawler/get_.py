# -*- coding: utf8 -*-
import re
import time
import xlrd
import xlwt
import json
import urllib
import urllib2
import chardet
import MySQLdb
import logging
import requests
import datetime
import lxml.html
import traceback
import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding(u"utf-8")


def connect_database(db_nick=u"yuqing"):  # 连接数据库
    conn = u""
    if db_nick == u"ProductData":
        while True:
            try:
                conn = MySQLdb.connect(host=u"192.168.16.17", user=u"wdzj_read", passwd=u"wdzj_read",
                                       db=u"ProductData", port=3306, charset=u"utf8")
                break
            except MySQLdb.Error, e:
                print u"Mysql Error %d: %s" % (e.args[0], e.args[1])
    elif db_nick == u"RawData":
        while True:
            try:
                conn = MySQLdb.connect(host=u"192.168.16.17", user=u"wdzj_read", passwd=u"wdzj_read",
                                       db=u"RawData", port=3306, charset=u"utf8")
                break
            except MySQLdb.Error, e:
                print u"Mysql Error %d: %s" % (e.args[0], e.args[1])
    else:
        print u"No such database!!!"
    return conn


def initlogging(logfilename):
    logging.basicConfig(
        level=logging.DEBUG,
        format=u"LINE %(lineno)-4d  %(levelname)-8s %(message)s",
        datefmt=u"%m-%d %H:%M",
        filename=logfilename,
        filemode=u"w")
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter(u"LINE %(lineno)-4d : %(levelname)-8s %(message)s")
    # tell the handler to use this format
    console.setFormatter(formatter)
    logging.getLogger(u"").addHandler(console)


def insert_(conn, cur, ):
    update_time = str(time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    insert_sql = u"INSERT INTO WDZJ_PLAT_COMPANY_IC_DATA () VALUES ('" + u"','" + + u"','" + + u"','" + \
                 + u"','" + u"','" + u"','" + update_time + u"')"
    try:
        cur.execute(insert_sql)
        conn.commit()
    except MySQLdb.Error:
        traceback.print_exc()
        pass


def climb_tianyan(sheet, file_name):
    new_workbook = xlwt.Workbook(file_name)
    sheet_w = new_workbook.add_sheet(sheet)
    yesterday = str(datetime.datetime.now().month) + u"月" + str(datetime.datetime.now().day - 1) + u"日"
    plat = []
    r = requests.session()
    r.headers = {u"User-Agent": u"Mozilla/5.0 (Windows NT 10.0, WOW64) "
                                u"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"}
    con = r.get(u"http://www.p2peye.com/shuju/ptsj/").text
    x = lxml.html.fromstring(con)
    plat_count = x.xpath(u"//*[@id='fixedptsj']/div/div/ul/li[5]/span/span/text()")
    result = {}
    for i in range(21, int(plat_count[0]) + 1):
        plat_name = x.xpath(u"//*[@id='platdata']/tbody/tr[" + str(i) + u"]/td[2]/a/text()")[0]
        loan_amount = x.xpath(u"//*[@id='platdata']/tbody/tr[" + str(i) + u"]/td[3]/text()")[0]
        result[plat_name] = loan_amount
    for nu, i in enumerate(plat):
        if i.decode(u"utf-8") in result.keys():
            sheet_w.write(nu, 0, i.decode(u"utf-8"))
            sheet_w.write(nu, 1, result[i.decode(u"utf-8")])
            sheet_w.write(nu, 2, yesterday.decode(u"utf-8"))
            print i, result[i.decode(u"utf-8")], yesterday
    new_workbook.save(file_name)


def climb_hujing(conn, cur, url):
    x = lxml.html.fromstring(r.get(url).text)  # .replace(u" u", u"").replace(u"\n", u"")
    plat_id = url.lstrip(u"")
    plat_name = x.xpath(u"//*[@id='theForm']/div[1]/div[2]/div[1]/div[1]/span[1]/text()")[0]
    tr = x.xpath(u"//*[@id='trade-log']/table[1]/tr")
    table2_td = x.xpath(u"//*[@id='trade-log']/table[2]/tr[2]/td")
    for i in range(2, len(tr) + 1):
        data_ls = []
        day_date = x.xpath(u"//*[@id='trade-log']/table[1]/tr[" + str(i) + u"]/td/text()")[0]
        create_time = str(time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        for j in range(1, len(table2_td) + 1):
            try:
                value = x.xpath(u"//*[@id='trade-log']/table[2]/tr[" + str(i) + u"]/td[" + str(j) + u"]/text()")[0]
                # .replace(u"\r\n", u"").replace(u"\n", u"").replace(u"\t", u"").replace(u" u", u"")
                if len(value):
                    data_ls.append(u"%.2f" % float(value))
                else:  # 为空
                    data_ls.append(value)
            except IndexError:
                # traceback.print_exc()
                data_ls.append(u"0.00")
                logging.warning(u"表格不足默认值设为0.00：%s,%s,%s,%s", plat_name, url, i, j)
        # [data_ls.append(u"0.00") for i in range(len(data_ls), 27)]
        while len(data_ls) < 27:
            data_ls.append(u"0.00")
        insert_finace_association_of_china(conn, cur, plat_id, plat_name, day_date, data_ls[0], data_ls[1], data_ls[2],
                                           data_ls[3].rstrip(u".00"), data_ls[4].rstrip(u".00"), data_ls[5],
                                           data_ls[6], data_ls[7], data_ls[8],
                                           data_ls[9], data_ls[10], data_ls[11], data_ls[12], data_ls[13],
                                           data_ls[14], data_ls[15], data_ls[16], data_ls[17], data_ls[18],
                                           data_ls[19], data_ls[20], data_ls[21], data_ls[22], data_ls[23],
                                           data_ls[24], data_ls[25], data_ls[26], url, create_time)


def get_info():
    first_url = u""
    x = lxml.html.fromstring(r.get(first_url).text)
    total_nu = x.xpath(u"//*[@id='oldpage']/a[13]/@href")[0].lstrip(u"")
    # select_sql = u"SELECT plat_name FROM finace_association_of_china"
    # app_management = pd.read_sql(select_sql, conn_yuqing)
    for i in range(1, int(total_nu) + 1):
        url_page = u"" + str(i)
        for j in lxml.html.fromstring(r.get(url_page).text).xpath(u"//*[@id='runinfotbody']/tr/td[8]/a/@href"):
            climb_hujing(conn_yuqing, cur, u"" + j)


def get_cookie():
    return u""
    
    
def get_proxies():
    ip = json.loads(requests.get(
            "http://dps.kuaidaili.com/api/getdps/?orderid=958964320330191&num=50&ut=1&format=json&sep=1").content)
    proxies = {  # 每次请求从代理ip中随机产生一个地址
        "http": "http://8283891:ojonvhe8@" + ip["data"]["proxy_list"][random.randint(0, len(ip)-1)]
    }
    return proxies


def login(r, username, pwd):
    m = hashlib.md5()
    m.update(pwd)
    logging.info(r.post('https://www..com/cd/login.json', data=json.dumps({'mobile': username, 'cdpassword': str(m.hexdigest()), 'loginway': 'PL', 'autoLogin': True})).text)
    return r


def main():
    initlogging(u"get_.log")
    logging.info(u"current:%s", time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    conn_yuqing_be = connect_database(db_nick=u"yuqing")
    cur_be = conn_yuqing_be.cursor()
    r = requests.session()
    r.headers = {
        u"User-Agent": u"Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 "
                       u"(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        # u"Cookie": get_cookie(),
        # u"X-Requested-With": u"XMLHttpRequest",
        # u"Host": u"www.tianyancha.com",
        # u"Host": u"www.tianyancha.com",
        # u"Connection": u"keep-alive",
        # u"Content-Length": u"106",
        # u"Origin": u"https://www.tianyancha.com",
        # u"Content-Type": u"application/json; charset=UTF-8",  # x-www-form-urlencoded
        # u"Accept": u"*/*",
        # u"Referer": u"https://www.tianyancha.com/login",
        # u"Accept-Encoding": u"gzip, deflate, br",
        # u"Accept-Language": u"zh-CN,zh;q=0.8"
    }
    # name_url = get_company_url(conn_yuqing)
    error_plat = u""  # 默认从第一条运行
    # error_plat = u""
    nu = 0
    while len(error_plat):
        time.sleep(1)
        # index = list(name_url.get(u"company_name")).index(error_plat)
        error_plat = get_info().decode(u"utf-8")
        nu += 1
        if nu % 9 == 0:  # 重复请求10次无果后停止运行
            break
    cur_be.close()
    conn_yuqing_be.close()
    print u"climb finish"


if __name__ == u"__main__":  # 测试函数
    main()
