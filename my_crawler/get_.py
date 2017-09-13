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
from bs4 import BeautifulSoup
# import sys
# reload(sys)
# sys.setdefaultencoding(u"utf-8")


def connect_database(db_nick=u""):  # 连接数据库
    conn = u""
    if db_nick == u"Data":
        while True:
            try:
                conn = MySQLdb.connect(host=u"", user=u"", passwd=u"",
                                       db=u"", port=3306, charset=u"utf8")
                break
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s", e.args[0], e.args[1])
    elif db_nick == u"Data":
        while True:
            try:
                conn = MySQLdb.connect(host=u"", user=u"", passwd=u"",
                                       db=u"", port=3306, charset=u"utf8")
                break
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s", e.args[0], e.args[1])
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
    insert_sql = u"INSERT INTO WDZJ_PLAT_COMPANY_IC_DATA () VALUES (" + u"','" + update_time + u"')"
    try:
        cur.execute(insert_sql)
        conn.commit()
    except MySQLdb.Error:
        logging.error(traceback.print_exc())
        pass


def climb_hujing(conn, cur, name_urls, index):
    # for url in name_urls[index:]:
    text = r.get(url).text  # .replace(u"\r\n", u"").replace(u"\n", u"").replace(u"\t", u"").replace(u" ", u"")
    x = lxml.html.fromstring(text)
    soup = BeautifulSoup(text, u"lxml")
    url = soup.find_all(u"a", class_=u"fn-left ui-box-username fn-text-overflow a_cor pl20")[0].string
    plat_id = url.lstrip(u"")
    plat_name = x.xpath(u'//*[@id="theForm"]/div[1]/div[2]/div[1]/div[1]/span[1]/text()')[0]
    tr = x.xpath(u'//*[@id="trade-log"]/table[1]/tr')
    table2_td = x.xpath(u'//*[@id="trade-log"]/table[2]/tr[2]/td')
    for i in range(2, len(tr) + 1):
        data_ls = []
        day_date = x.xpath(u'//*[@id="trade-log"]/table[1]/tr[" + str(i) + u"]/td/text()')[0]
        create_time = str(time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        for j in range(1, len(table2_td) + 1):
            try:
                value = x.xpath(u"" + str(i) + u"" + str(j) + u"]/text()")[0]
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
                                           data_ls[3], data_ls[4], data_ls[5],
                                           data_ls[6], data_ls[7], data_ls[8],
                                           data_ls[9], data_ls[10], data_ls[11], data_ls[12], data_ls[13],
                                           data_ls[14], data_ls[15], data_ls[16], data_ls[17], data_ls[18],
                                           data_ls[19], data_ls[20], data_ls[21], data_ls[22], data_ls[23],
                                           data_ls[24], data_ls[25], data_ls[26], url, create_time)


def get_info(conn_yuqing, cur, url):
    first_url = url
    x = lxml.html.fromstring(r.get(first_url).text)
    total_nu = x.xpath(u'//*[@id="oldpage"]/a[13]/@href')[0].lstrip(u"")
    for i in range(1, int(total_nu) + 1):
        url_page = u"" + str(i)
        for j in lxml.html.fromstring(r.get(url_page).text).xpath(u"//*[@id=\"runinfotbody\"]/tr/td[8]/a/@href"):
            climb_hujing(conn_yuqing, cur, u"" + j)


def get_url(conn):
    select_sql = u"SELECT  FROM "
    app_management = pd.read_sql(select_sql, conn)
    # name_urls = app_management.get("url")
    return app_management


def get_cookie():
    return u""
    
    
def get_proxies():
    ip = json.loads(requests.get(
            u"http://.com/api/").content)
    proxies = {  # 每次请求从代理ip中随机产生一个地址
        u"http": u"http://name:pwd@" + ip[u"data"][u"proxy_list"][random.randint(0, len(ip)-1)]
    }
    return proxies


def login(r, username, pwd):
    m = hashlib.md5()
    m.update(pwd)
    logging.info(r.post(u"https://www..com/cd/login.json", data=json.dumps({u"mobile": username, u"cdpassword":
                        unicode(m.hexdigest()), u"loginway": u"PL", u"autoLogin": True})).text)  # payload
    return r


def main():
    initlogging(u"get_.log")
    logging.info(u"current:%s", time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    conn_yuqing_be = connect_database(db_nick=u"")
    cur_be = conn_yuqing_be.cursor()
    r = requests.session()
    r.headers = {
        u"User-Agent": u"Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 "
                       u"(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        # u"Cookie": get_cookie(),
        # u"X-Requested-With": u"XMLHttpRequest",
        # u"Host": u"",
        # u"Content-Length": u"106",
        # u"Origin": u"",
        # u"Content-Type": u"application/json; charset=UTF-8",  # x-www-form-urlencoded
        # u"Accept": u"*/*",
        # u"Referer": u"",
        # u"Accept-Encoding": u"gzip, deflate, br",
        # u"Accept-Language": u"zh-CN,zh;q=0.8"
    }
    name_urls = list(get_url(conn_yuqing).get(u"url"))
    error_url = u""  # 默认从第一条运行
    # error_url = u""
    nu = 0
    while len(error_url):
        time.sleep(1)
        index = name_urls.index(error_url)
        error_url = get_info(conn_yuqing_be, cur_be, name_urls, index).decode(u"utf-8")
        nu += 1
        if nu % 9 == 0:  # 重复请求10次无果后停止运行
            break
    cur_be.close()
    conn_yuqing_be.close()
    logging.info(u"climb finish")


if __name__ == u"__main__":  # 测试函数
    main()
