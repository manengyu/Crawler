# -*- coding: utf8 -*-
import urllib
import urllib2
import requests
import re
import time
import xlrd
import xlwt
import chardet
import MySQLdb
import pandas as pd
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def climb_01(sheet, file_name):
    new_workbook = xlwt.Workbook(file_name)
    sheet_w = new_workbook.add_sheet(sheet)
    nu = 0
    plat = []
    pagecount = json.loads(requests.get('http://www.01caijing.com/remote/api.json?path=/p2p-api/platform/search.json&cond[pageIndex]=1').content)['data']['count']/100 + 1
    for i in range(1, pagecount + 1):
        url = 'http://www.01caijing.com/remote/api.json?path=/p2p-api/platform/search.json&cond[pageIndex]=' + str(i)
        data = json.loads(requests.get(url).content)
        for j in plat:
            for k in data['data']['data']:
                if j.decode('utf-8') in k.values():
                    platname = k['platname']  # 网址
                    data_amount = requests.get('http://www.01caijing.com/remote/api.json?path=%2Fp2p-api%2Fplatform%2Famount.json&cond%5Bwebsite%5D=' + platname + '&cond%5BgroupBy%5D=day').content
                    try:
                        loan_amount = json.loads(data_amount)['data'][-1][-1]
                    except:
                        loan_amount = ''
                    try:
                        date = json.loads(data_amount)['data'][-1][0]
                    except:
                        date = ''
                    sheet_w.write(nu, 0, j.decode('utf-8'))
                    sheet_w.write(nu, 1, loan_amount)
                    if date != '':
                        sheet_w.write(nu, 2, time.strftime('%m月%d日', time.localtime(float(date/1000))).decode('utf-8'))
                    nu += 1
    # new_workbook.save(file_name)


# 测试函数
if __name__ == "__main__":
    climb_01(u'Sheet1', u'01caijing.xls')



