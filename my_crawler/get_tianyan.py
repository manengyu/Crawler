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
    plat = [
        "汇理财",
"麻袋理财",
"易通贷",
"民贷天下",
"元宝365",
"恒易融",
"钱保姆",
"米缸金融",
"有融网",
"宜聚网",
"友金所",
"铜掌柜",
"福银票号",
"多赢",
"十六铺金融",
"壹佰金融",
"钱香",
"淘淘金",
"聚宝匯",
"宝象金融",
"浙财理财",
"投融家",
"钜宝盆",
"多多理财",
"泰然金融",
"联连理财",
"首金网",
"华赢贷",
"小九金服",
"森昊好时贷",
"来存吧",
"普惠家",
"新升贷",
"欢乐合家",
"新城金融",
"信和大金融",
"华人金融",
"联金所",
"旺财谷",
"钱盆网",
"91旺财",
"拓道金服",
"金融工场",
"博金贷",
"点融网",
"地标金融",
"东方汇",
"宜贷网",
"365易贷",
"翼龙贷",
"财富中国",
"付融宝",
"开鑫贷",
"冠e通",
"广信贷",
"好贷宝",
"合拍在线",
"合时代",
"和信贷",
"汇盈金服",
"理想宝",
"众信金融",
"爱钱帮",
"爱钱进",
"融贝网",
"爱投资",
"积木盒子",
"金联储",
"金票通",
"金信网",
"金银猫",
"金桥梁",
"金融圈",
"君融贷",
"聚有财",
"可溯金融",
"金开贷",
"口袋理财",
"礼德财富",
"连资贷",
"理财范",
"红岭创投",
"新联在线",
"你我贷",
"诺诺镑客",
"恒信易贷",
"鹏金所",
"拍拍贷",
"PPmoney",
"口贷网",
"钱爸爸",
"人人贷",
"人人聚财",
"小微金融",
"融金所",
"投哪网",
"丁丁贷",
"团贷网",
"图腾贷",
"网利宝",
"微贷网",
"共信赢",
"温商贷",
"温州贷",
"向上金服",
"小牛在线",
"小猪理财",
"鑫合汇",
"信融财富",
"信用宝",
"银湖网",
"银票网",
"一起好",
"宜人贷",
"有利网",
"招商贷",
"珠宝贷",
"中瑞财富"]
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



