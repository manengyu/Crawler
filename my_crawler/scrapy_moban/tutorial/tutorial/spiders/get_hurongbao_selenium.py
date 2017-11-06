# -*-coding:utf-8-*-
import re
import time
import MySQLdb
import requests
import traceback
from bs4 import BeautifulSoup
from selenium import webdriver
from huochetou_tocode.pipelines import HuochetouTocodePipeline
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Gsxt(object):
    def __init__(self, br_name="phantomjs", r=u""):
        self.br = self.get_webdriver(br_name)
        self.wait = WebDriverWait(self.br, 10, 1.0)
        self.br.set_page_load_timeout(480)  # 设置网页加载超时时间
        self.br.set_script_timeout(480)
        self.r = self.br
        self.conn = HuochetouTocodePipeline.connect_database(db_nick=u"RawData")
        self.cur = self.conn.cursor()
    
    def input_params(self, multi_type, page_total, company_url):
        time.sleep(5)
        self.br.get(company_url)
        # oldtab = self.br.current_window_handle
        # self.br.find_element_by_xpath(
        #     u"//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[2]/input").send_keys(
        #     u"")
        # self.br.find_element_by_xpath(
        #     u"//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[3]/input").send_keys(
        #     u"")
        # action = ActionChains(self.br)
        # element = self.wait_for(By.ID, u"next")
        # element = self.wait_for(By.XPATH, u"//ul[@class='nav']/li[7]/a")
        # element = self.br.find_element_by_xpath(u"//a[@id='next']")
        # action.click(element).perform()  # 鼠标点击事件
        # element.click()
        # print loan_urls
        # MyParse(loan_urls, self.r)
        # newtab = self.br.current_window_handle
        # self.br.switch_to_window()
        if u"all" == multi_type:
            for i in range(int(page_total)):
                count = i
                while count:
                    js = u"document.getElementById('next').click();"
                    self.br.execute_script(js)
                    count -= 1
                    time.sleep(0.5)
                soup = BeautifulSoup(self.br.page_source, u"lxml")
                loan_urls = []
                for j in soup.find_all(u"a", id=u"title"):
                    # loan_urls.append(j.contents[0])
                    loan_urls.append(u"https://www.0080.cn/finance/product_list.html?" + j[u'href'].split(u"?")[1])
                try:
                    print loan_urls
                    MyParse(loan_urls, self.r, self.conn, self.cur)
                except:
                    traceback.print_exc()
                    return
                self.br.get(company_url)
                time.sleep(2)
        elif u"noviceArea" == multi_type:
            js = u"document.getElementById('noviceArea').click();"
            self.br.execute_script(js)
            page_total = BeautifulSoup(self.br.page_source, u"lxml").find_all(u"a", id=u"last")[0].string
            page_total = 5
            for i in range(int(page_total)):
                js = u"document.getElementById('noviceArea').click();"
                self.br.execute_script(js)
                count = i
                while count:
                    js = u"document.getElementById('next').click();"
                    self.br.execute_script(js)
                    count -= 1
                    time.sleep(0.5)
                soup = BeautifulSoup(self.br.page_source, u"lxml")
                loan_urls = []
                for j in soup.find_all(u"a", id=u"title"):
                    # loan_urls.append(j.contents[0])
                    loan_urls.append(u"https://www.0080.cn/finance/product_list.html?" + j[u'href'].split(u"?")[1])
                try:
                    print loan_urls
                    MyParse(loan_urls, self.r, self.conn, self.cur)
                except:
                    traceback.print_exc()
                    return
                self.br.get(company_url)
                time.sleep(2)
        # for i in range(int(page_total)-1):
        #     time.sleep(5)
        #     print self.br.current_url
        #     print self.br.page_source
        #     return 0
        # action.release()
        # time.sleep(5)
        # self.br.get(company_url)
        # multi_content = []
        # for i in range(0, page_total - 1):  # js只能在一个元素下确定另一个元素
        #     js = u"document.querySelectorAll('[change-type=\"" + multi_type + \
        #          u"\"]')[0].getElementsByClassName('pagination-next  ')[0].getElementsByTagName('a')[
        # 0].click();"
        #     self.br.execute_script(js)
        #     multi_content.append(self.br.page_source)
        #     self.br.get(u"")
        #     time.sleep(5)
        # time.sleep(1.1)
        return 0#multi_content
    
    def wait_for(self, by1, by2):
        return self.wait.until(ec.presence_of_element_located((by1, by2)))
    
    def run(self, multi_type, page_total, url, loan_urls):
        # for i in [u'', u''][::-1]:
        # try:
        #     print loan_urls
        #     MyParse(loan_urls, self.r)
        # except:
        #     traceback.print_exc()
        #     return
        # return
        multi_content = self.hack_geetest(multi_type, page_total, url)
        time.sleep(1)
        self.quit_webdriver()
        return multi_content
    
    def hack_geetest(self, multi_type, page_total, company_url):
        return self.input_params(multi_type, page_total, company_url)
    
    def quit_webdriver(self):
        self.br.quit()
    
    @staticmethod
    def get_webdriver(name):
        if name.lower() == "phantomjs":
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap[u"phantomjs.page.settings.userAgent"] = (
                u"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36"
                u" (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36")
            return webdriver.PhantomJS(desired_capabilities=dcap)
            # headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            #            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            #            'Connection': 'keep-alive',
            #            "Cookie": ""
            #            }
            # for key, value in headers.iteritems():
            #     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
            # driver = webdriver.PhantomJS()
            # return driver
        elif name.lower() == u"chrome":
            return webdriver.Chrome()


class MyParse:
    def __init__(self, loan_urls=u'', rq=u"", conn=u"", cur=u""):
        self.r = rq
        self.conn = conn
        self.cur = cur
        self.handles_urls(loan_urls)

    def handles_urls(self, loan_urls):
        for i in loan_urls:
            self.r.get(i)
            text = self.r.page_source
            cookie = [item["name"] + "=" + item["value"] for item in self.r.get_cookies()]
            cookiestr = ';'.join(item for item in cookie)
            bid_url = re.findall(u"(\./product_info\.html\?\d+-\d+\.IBehaviorListener\.0-body-form-conExtendInfo-lnkTenderRecord.*?)\"",
                                 text)
            bid_url = bid_url[0]
            financeEndtime = re.findall(u"financeEndtime\" value=\"(.*?)\"", text)[0]
            data_dic = {u"form_hf_0": u"", u"financeEndtime": financeEndtime, u"isChkFlg": u"",
                        u"isChkFlgJXQ": u"", u"conExtendInfo:lnkTenderRecord": u"1"}
            headers = {
                u"User-Agent": u"Mozilla/5.0 (Windows NT 10.0, WOW64) AppleWebKit/537.36 "
                               u"(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
                u"X-Requested-With": u"XMLHttpRequest",
                u"Wicket-FocusedElementId": u"lnkTenderRecord",
                u"Wicket-Ajax": u"true",
                u"Wicket-Ajax-BaseURL": u"finance/product_info.html?" + bid_url.split(u"?")[1].split(u"-")[0] +
                                        u"&amp;" + bid_url.split(u"&")[-1],
                u"cookie": cookiestr
            }
            text_bid = requests.post(u"https://www.0080.cn/finance" + bid_url.lstrip(u"."), headers=headers, data=data_dic).text
            self.get_data(text, text_bid, bid_url)
            time.sleep(1)

    def get_data(self, text, text_bid, bid_url):
        soup = BeautifulSoup(text, u"lxml")
        url = u"https://www.0080.cn/finance/product_info.html?" + bid_url.split(u"?")[1].split(u"-")[0] + u"&" +\
              bid_url.split(u"&")[-1]
        loan_id = self.get_loan_id(bid_url)
        title = self.get_title(soup, text)
        amount = self.get_amount(soup, text)
        rate = self.get_rate(soup, text)
        rate_type = self.get_rate_type(soup, text)
        reward = self.get_reward(soup, text)
        reward_type = self.get_reward_type(soup, text)
        peroid = self.get_peroid(soup, text)
        peroid_type = self.get_peroid_type(soup, text)
        loan_time = self.get_loan_time(soup, text)
        way = self.get_way(soup, text)
        progress = self.get_progress(soup, text)
        soup_bid = BeautifulSoup(text_bid, u"lxml")
        bid_name = self.get_bid_name(soup_bid, text_bid)
        bid_amount = self.get_bid_amount(soup_bid, text_bid)
        bid_time = self.get_bid_time(soup_bid, text_bid)
        plat_id = self.get_plat_id()
        # print bid_name, bid_amount, bid_time
        # print plat_id, loan_id, title, amount, rate, rate_type, u"0", peroid, way, progress, peroid_type, u"admin", loan_time
        try:
            HuochetouTocodePipeline.insert_borrow(self.conn, self.cur,)
            for nu, j in enumerate(zip(bid_name, bid_amount, bid_time)):
                HuochetouTocodePipeline.insert_bid(self.conn, self.cur,)
                print j[0], j[1], j[2]
        except MySQLdb.IntegrityError:
            pass
    
    @staticmethod
    def get_loan_id(*args):
        return args[0].split(u"=")[-1]

    @staticmethod
    def get_title(*args):
        return args[0].find_all(u"span", id=u"title")[0].string

    @staticmethod
    def get_amount(*args):
        res = args[0].find_all(u"b", id=u"amount")[0].string.replace(u",", u"")
        if u"万" in res:
            return (res.replace(u"万", u""))*10000
        else:
            return res

    @staticmethod
    def get_rate(*args):
        return args[0].find_all(u"b", id=u"rate")[0].string.replace(u"%", u"")

    @staticmethod
    def get_rate_type(*args):
        return u"年"

    @staticmethod
    def get_reward(*args):
        return u""

    @staticmethod
    def get_reward_type(*args):
        return u""

    @staticmethod
    def get_peroid(*args):
        return args[0].find_all(u"b", id=u"period")[0].string

    @staticmethod
    def get_peroid_type(*args):
        peroid = u"".join(args[0].find_all(u"b", id=u"period")[0].parent.strings)
        if u"天" in peroid or u"日" in peroid:
            return u"天"
        elif u"月" in peroid:
            return u"月"
        elif u"年" in peroid:
            return u"年"

    @staticmethod
    def get_loan_time(*args):
        return args[0].find_all(u"em", id=u"publishDate")[0].string

    @staticmethod
    def get_way(*args):
        res = re.findall(u"还款方式： </span><span style=\"color: #444;\">(.*?)</span>", args[1])[0]
        if u"一次性" in res \
                or u"付息还本" in res \
                or u"到期全额" in res \
                or u"到期还本付息" in res \
                or u"到期还本还息" in res \
                or u"到期付息还本" in res \
                or u"到期归还本金" in res \
                or u"按天" in res \
                or u"按日" in res:
            return u"到期还本息"
        elif u"每月付息" in res \
                or u"每月还息" in res \
                or u"按月付息" in res \
                or u"按月还息" in res \
                or u"按期" in res:
            return u"每月付息到期还本"
        elif u"按月分期" in res \
                or u"等额" in res:
            return u"每月分期"
        elif u"按季" in res:
            return u"每季分期"

    @staticmethod
    def get_progress(*args):
        return args[0].find_all(u"em", id=u"progress")[0].string.replace(u"%", u"")

    @staticmethod
    def get_bid_name(*args):
        res = []
        for i in args[0].find_all(u"tr", id=re.compile(u"tenderRecordList-")):
            res.append(i.contents[3].string)
        return res

    @staticmethod
    def get_bid_amount(*args):
        res = []
        for i in args[0].find_all(u"tr", id=re.compile(u"tenderRecordList-")):
            res.append(i.contents[5].string.replace(u",", u""))
        return res

    @staticmethod
    def get_bid_time(*args):
        res = []
        for i in args[0].find_all(u"tr", id=re.compile(u"tenderRecordList-")):
            res.append(u"20" + i.contents[7].string.replace(u"/", u"-"))
        return res

    @staticmethod
    def get_plat_id():
        return u"0080"

# if __name__ == u"__main__":
#     Gsxt("chrome").run(multi_type, page_total, url)
