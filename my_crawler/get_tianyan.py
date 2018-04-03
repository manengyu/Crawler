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
import json
import lxml.html
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def climb_tianyan(sheet, file_name):
    new_workbook = xlwt.Workbook(file_name)
    sheet_w = new_workbook.add_sheet(sheet)
    yesterday = str(datetime.datetime.now().month) + '月' + str(datetime.datetime.now().day - 1) + '日'
    plat = []
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


# 测试函数
if __name__ == "__main__":
    climb_tianyan(u'Sheet1', u'tianyan.xls')



