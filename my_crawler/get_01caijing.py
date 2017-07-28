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


def climb_01(sheet, file_name):
    new_workbook = xlwt.Workbook(file_name)
    sheet_w = new_workbook.add_sheet(sheet)
    nu = 0
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



