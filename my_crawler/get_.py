# -*- coding: utf8 -*-
import urllib
import urllib2
import requests
import re
import time
import datetime
import xlrd
import xlwt
import chardet
import MySQLdb
import pandas as pd
import logging
import json
import lxml.html
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# 连接数据库
def connect_database(db_nick='yuqing'):
    if db_nick == 'ProductData':
        while True:
            try:
                conn = MySQLdb.connect(host='192.168.16.17', user='wdzj_read', passwd='wdzj_read',
                                       db='ProductData', port=3306, charset='utf8')
                break
            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    elif db_nick == 'RawData':
        while True:
            try:
                conn = MySQLdb.connect(host='192.168.16.17', user='wdzj_read', passwd='wdzj_read',
                                       db='RawData', port=3306, charset='utf8')
                break
            except MySQLdb.Error, e:
                print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    else:
        print 'No such database!!!'
    return conn


def insert_WDZJ_PLAT_COMPANY_IC_DATA21(conn, cur, COMPANY_NAME, IC_DATA, SHAREHOLDER_DATA, PRINCIPAL_DATA, INVESTMENT_ABROAD, SOURCE_URL):
    UPDATE_DATE = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    insert_sql = "INSERT INTO WDZJ_PLAT_COMPANY_IC_DATA ( COMPANY_NAME, IC_DATA, SHAREHOLDER_DATA," \
                 " PRINCIPAL_DATA, INVESTMENT_ABROAD, SOURCE_URL, UPDATE_DATE) VALUES ('" + COMPANY_NAME + "','" +\
                 IC_DATA + "','" + SHAREHOLDER_DATA + "','" + PRINCIPAL_DATA + "','" + INVESTMENT_ABROAD + "','" +\
                 SOURCE_URL + "','" + UPDATE_DATE + "')"
    try:
        cur.execute(insert_sql)
        conn.commit()
    except:
        traceback.print_exc()
        pass


def climb_tianyan(sheet, file_name):
    new_workbook = xlwt.Workbook(file_name)
    sheet_w = new_workbook.add_sheet(sheet)
    yesterday = str(datetime.datetime.now().month) + '月' + str(datetime.datetime.now().day - 1) + '日'
    plat = [

]
    r = requests.session()
    r.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",}
    con = r.get('http://www.p2peye.com/shuju/ptsj/').text
    x = lxml.html.fromstring(con)
    plat_count = x.xpath('//*[@id="fixedptsj"]/div/div/ul/li[5]/span/span/text()')
    result = {}
    for i in range(21, int(plat_count[0]) + 1):
        plat_name = x.xpath('//*[@id="platdata"]/tbody/tr[' + str(i) + ']/td[2]/a/text()')[0]
        loan_amount = x.xpath('//*[@id="platdata"]/tbody/tr[' + str(i) + ']/td[3]/text()')[0]
        result[plat_name] = loan_amount
    for nu, i in enumerate(plat):
        if i.decode('utf-8') in result.keys():
            sheet_w.write(nu, 0, i.decode('utf-8'))
            sheet_w.write(nu, 1, result[i.decode('utf-8')])
            sheet_w.write(nu, 2, yesterday.decode('utf-8'))
            print i, result[i.decode('utf-8')], yesterday
    new_workbook.save(file_name)


def climb_hujing(conn, cur, url):
    x = lxml.html.fromstring(r.get(url).text)  # .replace(' ', '').replace('\n', '')
    plat_id = url.lstrip('')
    plat_name = x.xpath('//*[@id="theForm"]/div[1]/div[2]/div[1]/div[1]/span[1]/text()')[0]
    tr = x.xpath('//*[@id="trade-log"]/table[1]/tr')
    table2_td = x.xpath('//*[@id="trade-log"]/table[2]/tr[2]/td')
    for i in range(2, len(tr) + 1):
        data_ls = []
        day_date = x.xpath('//*[@id="trade-log"]/table[1]/tr[' + str(i) + ']/td/text()')[0]
        create_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        for j in range(1, len(table2_td) + 1):
            try:
                value = x.xpath('//*[@id="trade-log"]/table[2]/tr[' + str(i) + ']/td[' + str(j) + ']/text()')[0]  # .replace('\r\n', '').replace('\n', '').replace('\t', '').replace(' ', '')
                if len(value):
                    data_ls.append('%.2f' % float(value))
                else:  # 为空
                    data_ls.append(value)
            except:
                # traceback.print_exc()
                data_ls.append('0.00')
                logging.warning(u'表格不足默认值设为0.00：%s,%s,%s,%s', plat_name, url, i, j)
        [data_ls.append('0.00') for i in range(len(data_ls), 27)]
        insert_finace_association_of_china(conn, cur, plat_id, plat_name, day_date, data_ls[0], data_ls[1], data_ls[2],
                                           data_ls[3].rstrip('.00'), data_ls[4].rstrip('.00'), data_ls[5], data_ls[6], data_ls[7], data_ls[8],
                                           data_ls[9], data_ls[10], data_ls[11], data_ls[12], data_ls[13],
                                           data_ls[14], data_ls[15], data_ls[16], data_ls[17], data_ls[18],
                                           data_ls[19], data_ls[20], data_ls[21], data_ls[22], data_ls[23],
                                           data_ls[24], data_ls[25], data_ls[26], url, create_time)


def get_info():
    first_url = ''
    x = lxml.html.fromstring(r.get(first_url).text)
    total_nu = x.xpath('//*[@id="oldpage"]/a[13]/@href')[0].lstrip('')
    # select_sql = "SELECT plat_name FROM finace_association_of_china"
    # app_management = pd.read_sql(select_sql, conn_yuqing)
    for i in range(1, int(total_nu) + 1):
        url_page = '' + str(i)
        for j in lxml.html.fromstring(r.get(url_page).text).xpath('//*[@id="runinfotbody"]/tr/td[8]/a/@href'):
            climb_hujing(conn_yuqing, cur, '' + j)


def main():
    logging.warning("current:%s",time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    conn_yuqing_be = connect_database(db_nick='yuqing')
    cur_be = conn_yuqing_be.cursor()
    r = requests.session()
    r.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
        # "Cookie": get_cookie(),
        # 'X-Requested-With': 'XMLHttpRequest',
        # 'Host': 'www.tianyancha.com',
        # 'Host': 'www.tianyancha.com',
        # 'Connection': 'keep-alive',
        # 'Content-Length': '106',
        # 'Origin': 'https://www.tianyancha.com',
        # 'Content-Type': 'application/json; charset=UTF-8',  # x-www-form-urlencoded
        # 'Accept': '*/*',
        # 'Referer': 'https://www.tianyancha.com/login',
        # 'Accept-Encoding': 'gzip, deflate, br',
        # 'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    name_url = get_company_url(conn_yuqing)
    error_plat = u""  # 默认从第一条运行
    # error_plat = u""
    nu = 0
    while len(error_plat):
        time.sleep(1)
        index = list(name_url.get('company_name')).index(error_plat)
        error_plat = get_info(conn_yuqing, cur, conn_yuqing_be, cur_be, r, conn_yuqing_21, cur_21, name_url,
                              index).decode("utf-8")
        nu += 1
        if nu % 9 == 0:  # 重复请求10次无果后停止运行
            break
    cur_be.close()
    conn_yuqing_be.close()
    print "climb finish"


# 测试函数
if __name__ == "__main__":
    main()
    



