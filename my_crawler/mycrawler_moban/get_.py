# -*- coding: utf8 -*-
import re
import time
import xlrd
import xlwt
import json
import random
import urllib
import urllib2
import chardet
import hashlib
import requests
import lxml.html
import traceback
from bs4 import BeautifulSoup
from database import mylogging as logging
from sql import insert_sql, delete_sql, update_sql, select_sql
# import sys
# reload(sys)
# sys.setdefaultencoding(u"utf-8")


class Crawler:
    def __init__(self):
        self.main()

    def climb_hujing(self, r, name_urls, index):
        # for url in name_urls[index:]:
        text = r.get(name_urls[index]).text
        # .replace(u"\r\n", u"").replace(u"\n", u"").replace(u"\t", u"").replace(u" ", u"")
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
            update_time = unicode(time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
            tmp = (plat_id, plat_name, day_date, data_ls[0], data_ls[1],
                                                    data_ls[2], data_ls[3], data_ls[4], data_ls[5],
                                                    data_ls[6], data_ls[7], data_ls[8],
                                                    data_ls[9], data_ls[10], data_ls[11], data_ls[12], data_ls[13],
                                                    data_ls[14], data_ls[15], data_ls[16], data_ls[17], data_ls[18],
                                                    data_ls[19], data_ls[20], data_ls[21], data_ls[22], data_ls[23],
                                                    data_ls[24], data_ls[25], data_ls[26], url, create_time)
    
    def get_info(self, r, url, index):
        first_url = url
        x = lxml.html.fromstring(r.get(first_url).text)
        total_nu = x.xpath(u'//*[@id="oldpage"]/a[13]/@href')[0].lstrip(u"")
        for i in range(1, int(total_nu) + 1):
            url_page = u"" + str(i)
            for j in lxml.html.fromstring(r.get(url_page).text).xpath(u"//*[@id=\"runinfotbody\"]/tr/td[8]/a/@href"):
                self.climb_hujing(r, u"" + j, index)
    
    @staticmethod
    def get_url():
        # name_urls = app_management.get("url")
        return True
    
    @staticmethod
    def get_proxies():
        ip = json.loads(requests.get(
                u"http://.com/api/").content)
        proxies = {  # 每次请求从代理ip中随机产生一个地址
            u"http": u"http://name:pwd@" + ip[u"data"][u"proxy_list"][random.randint(0, len(ip)-1)]
        }
        return proxies
    
    @staticmethod
    def login(r, username, pwd):
        m = hashlib.md5()
        m.update(pwd)
        logging.info(r.post(u"https://www..com/cd/login.json", data=json.dumps({u"mobile": username, u"cdpassword":
                            unicode(m.hexdigest()), u"loginway": u"PL", u"autoLogin": True})).text)  # payload
        return r
    
    def main(self):
        logging.info(u"start:current:%s", time.strftime(u"%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
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
        name_urls = list(self.get_url().get(u"url"))
        error_url = u""  # 默认从第一条运行
        # error_url = u""
        nu = 0
        while len(error_url):
            time.sleep(1)
            index = name_urls.index(error_url)
            error_url = self.get_info(r, name_urls, index).decode(u"utf-8")
            nu += 1
            if nu % 9 == 0:  # 重复请求10次无果后停止运行
                break
        logging.info(u"climb finish")


if __name__ == u"__main__":  # 测试函数
    Crawler()
