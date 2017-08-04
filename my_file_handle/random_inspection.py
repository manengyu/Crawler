#coding:utf-8
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


def out_my_data(sheet, file_path, arg, user_name):
    workbook = xlrd.open_workbook(file_path)
    booksheet = workbook.sheet_by_name(sheet)
    ls = []
    for row in range(booksheet.nrows):
        if booksheet.cell(row, 4).value == user_name:
            if arg == "date":
                tuple_date = xlrd.xldate_as_tuple(booksheet.cell(row, 5).value, 0)
                str_date = str(tuple_date[0]).decode("utf-8") + u"/" + str(tuple_date[1]).decode("utf-8") + u"/" +\
                           str(tuple_date[2]).decode("utf-8")
                if str_date not in ls:
                    ls.append(str_date)
            else:
                for i in range(15):
                    if arg == "plat_name":
                        ls.append(booksheet.cell(row, 1).value)
                        # print booksheet.cell(row, 1).value
                    if arg == "user_name":
                        ls.append(booksheet.cell(row, 4).value)
                        # print booksheet.cell(row, 3).value
                    if arg == "way":
                        ls.append(booksheet.cell(row, 3).value)
                        # print booksheet.cell(row, 3).value
    return ls


def save_my_data(file_name, sheet, ls_name, ls_plat, ls_way, ls_date, dict_biao):
    new_workbook = xlwt.Workbook(file_name)
    sheet_w = new_workbook.add_sheet(sheet)
    title = [u"姓名", u"平台名", u"平台网址", u"采集方式", u"抽查时间", u"被抽查时间", u"标ID", u"成交量", u"是否存在问题", u"是否联系修改", u"平台反馈"]
    for j in range(0, len(title)):
        sheet_w.write(0, j, title[j])
    for i in range(len(ls_name)):
        sheet_w.write(i + 1, 0, ls_name[i])
    for i in range(len(ls_plat)):
        sheet_w.write(i + 1, 1, ls_plat[i])
        sheet_w.write(i + 1, 2, dict_biao[ls_plat[i]]['loan_url'][i % 15])
        sheet_w.write(i + 1, 5, dict_biao[ls_plat[i]]['SUCCESS_TIME_DATE'][i % 15])
        sheet_w.write(i + 1, 6, dict_biao[ls_plat[i]]['loan_id'][i % 15])
        sheet_w.write(i + 1, 7, dict_biao[ls_plat[i]]['amount'][i % 15])
        sheet_w.write(i + 1, 9, dict_biao[ls_plat[i]]['repayment_type'][i % 15])
        sheet_w.write(i + 1, 10, dict_biao[ls_plat[i]]['loan_type'][i % 15])
        sheet_w.write(i + 1, 11, dict_biao[ls_plat[i]]['interest_rate'][i % 15])
        sheet_w.write(i + 1, 12, dict_biao[ls_plat[i]]['loan_period'][i % 15])
    for i in range(len(ls_way)):
        sheet_w.write(i + 1, 3, ls_way[i])
    for nu, i in enumerate(ls_date):
        [sheet_w.write(nu*75 + j + 1, 4, i) for j in range(75)]
    new_workbook.save(file_name)


def selectdata(ls_plat):
    conn_ProductData = connect_database(db_nick='ProductData')
    conn_RawData = connect_database(db_nick='RawData')
    dict_re = {}
    ls_plat = [ls_plat[i] for i in range(0, len(ls_plat), 15)]
    fields = ['loan_id', 'amount', 'loan_url', 'SUCCESS_TIME_DATE', 'repayment_type', 'loan_type', 'interest_rate', 'loan_period']
    for i in ls_plat:
        select_sql_ProductData = "select plat_id from shuju_plat_config where plat_name ='" + i + "'"
        plat_id = pd.read_sql(select_sql_ProductData, conn_ProductData).get('plat_id')[0]
        select_sql_RawData = u"select bor.loan_name,bor.loan_id,bor.amount,bor.interest_rate,bor.reward," \
                             u"bor.loan_period,bor.repayment_type,bor.loan_type,bor.loan_url,DATE_FORMAT(bor." \
                             u"SUCCESS_TIME_DATE, '%Y/%m/%d') as SUCCESS_TIME_DATE,count(DISTINCT bid.bidder_name) " \
                             u"sumbidder from borrow_list_" + plat_id + u" bor left join bid_record_" + plat_id + \
                             u" bid on bor.loan_id = bid.loan_id WHERE success_time_date >= '2017-06-01' and " \
                             u"loan_type not LIKE '%债%' group by bor.loan_id ORDER BY RAND() LIMIT 15"  # 抽查近一个月数据
        data = pd.read_sql(select_sql_RawData, conn_RawData)
        dict_re[i] = {}
        for j in fields:
            dict_re[i][j] = []
        if len(data) == 15:
            for j in data.iterrows():
                for k in fields:
                    dict_re[i][k].append(j[1][k])
        else:  # 如果当月无数据，默认为空
            for j in range(0, 15):
                for k in fields:
                    dict_re[i][k].append('')
        # print dict_re
    return dict_re


def main(sheet, file_path, user_name):
    ls_name = out_my_data(sheet, file_path, "user_name", user_name)  # user_name plat_name way date
    ls_plat = out_my_data(sheet, file_path, "plat_name", user_name)  # user_name plat_name way date
    ls_way = out_my_data(sheet, file_path, "way", user_name)  # user_name plat_name way date
    ls_date = out_my_data(sheet, file_path, "date", user_name)  # user_name plat_name way date
    file_name = u"数据抽查" + re.findall("[\d.-]+", file_path)[0].rstrip(".").decode("utf-8") + u"_" + user_name + u".xls"
    dict_biao = selectdata(ls_plat)
    save_my_data(file_name, sheet, ls_name, ls_plat, ls_way, ls_date, dict_biao)


# 测试函数
if __name__ == "__main__":
    main(u'Sheet1', ur'D:\cncepgf\workspace\抽查\抽查平台名单07.07-07.28.xlsx', u"马能宇")  # 工作表 文件所在路径 名字



