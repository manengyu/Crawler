#coding:utf-8
import urllib
import urllib2
import requests
import re
import time
import xlrd
import xlwt
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


def read_xls(sheet, file_path, *args):
    workbook = xlrd.open_workbook(file_path)
    booksheet = workbook.sheet_by_name(sheet)
    ls = []
    for row in range(booksheet.nrows):
        if booksheet.cell(row, 4).value == args[1]:
            if args[0] == "date":
                tuple_date = xlrd.xldate_as_tuple(booksheet.cell(row, 5).value, 0)  # 读取日期时
                str_date = str(tuple_date[0]).decode("utf-8") + u"/" + str(tuple_date[1]).decode("utf-8") + u"/" +\
                           str(tuple_date[2]).decode("utf-8")
                if str_date not in ls:
                    ls.append(str_date)
                ls.append(booksheet.cell(row, 1).value)
                ls.append(booksheet.cell(row, 2).value)
                ls.append(booksheet.cell(row, 3).value)
    return ls


def save_my_data(file_name, sheet, ls_name):
    new_workbook = xlwt.Workbook(file_name)
    sheet_w = new_workbook.add_sheet(sheet)
    title = [u"姓名", u"名", u"网址", u"方式", u"时间"]
    for j in range(0, len(title)):
        sheet_w.write(0, j, title[j])
    for i in range(len(ls_name)):
        sheet_w.write(i + 1, 0, ls_name[i])
    new_workbook.save(file_name)


def main(sheet, file_path, user_name):
    ls_name = read_xls(sheet, file_path, "user_name", user_name)  
    save_xls(file_name, sheet, ls_name)


# 测试函数
if __name__ == "__main__":
    main(u'Sheet1', ur'D:\cncepgf\workspace\07.07-07.28.xlsx', u"马能宇")  # 工作表 文件所在路径 名字



