# -*-coding:utf-8-*-
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Gsxt(object):
    def __init__(self, br_name="phantomjs"):
        self.br = self.get_webdriver(br_name)
        self.wait = WebDriverWait(self.br, 10, 1.0)
        self.br.set_page_load_timeout(480)  # 设置网页加载超时时间
        self.br.set_script_timeout(480)
    
    def input_params(self, multi_type, page_total, company_url):
        time.sleep(5)
        self.br.get(company_url)
        self.br.find_element_by_xpath(
            u"//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[2]/input").send_keys(
            u"")
        self.br.find_element_by_xpath(
            u"//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[3]/input").send_keys(
            u"")
        element = self.wait_for(By.XPATH,
                                u"//div[@class='modulein modulein1 mobile_box pl30 pr30 f14 collapse in']/div[5]")
        action = ActionChains(self.br)
        action.click(element).perform()  # 鼠标点击事件
        action.release()
        time.sleep(5)
        self.br.get(company_url)
        multi_content = []
        for i in range(0, page_total - 1):  # js只能在一个元素下确定另一个元素
            js = u"document.querySelectorAll('[change-type=\"" + multi_type + \
                 u"\"]')[0].getElementsByClassName('pagination-next  ')[0].getElementsByTagName('a')[0].click();"
            self.br.execute_script(js)
            multi_content.append(self.br.page_source)
            self.br.get(u"")
            time.sleep(5)
        time.sleep(1.1)
        return multi_content
    
    def wait_for(self, by1, by2):
        return self.wait.until(ec.presence_of_element_located((by1, by2)))
    
    def run(self, multi_type, page_total, url):
        # for i in [u'', u''][::-1]:
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

# if __name__ == u"__main__":
#     Gsxt("chrome").run(multi_type, page_total, url)
