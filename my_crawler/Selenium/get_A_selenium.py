# -*-coding:utf-8-*-
import time
import base64
from selenium import webdriver
from urllib.parse import quote
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
			# from selenium.webdriver.chrome.options import Options #  无头模式
			# chrome_options = Options()
			# chrome_options.add_argument(u'--headless')
			# chrome_options.add_argument(u'--disable-gpu')
			# return webdriver.Chrome(chrome_options=chrome_options)
            return webdriver.Chrome()

# if __name__ == u"__main__":
#     Gsxt("chrome").run(multi_type, page_total, url)

# get blob url
def get_file_content_chrome(driver, uri):
    result = driver.execute_async_script("""
    var uri = arguments[0];
    var callback = arguments[1];
    var toBase64 = function(buffer){for(var r,n=new Uint8Array(buffer),t=n.length,a=new Uint8Array(4*Math.ceil(t/3)),i=new Uint8Array(64),o=0,c=0;64>c;++c)i[c]="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".charCodeAt(c);for(c=0;t-t%3>c;c+=3,o+=4)r=n[c]<<16|n[c+1]<<8|n[c+2],a[o]=i[r>>18],a[o+1]=i[r>>12&63],a[o+2]=i[r>>6&63],a[o+3]=i[63&r];return t%3===1?(r=n[t-1],a[o]=i[r>>2],a[o+1]=i[r<<4&63],a[o+2]=61,a[o+3]=61):t%3===2&&(r=(n[t-2]<<8)+n[t-1],a[o]=i[r>>10],a[o+1]=i[r>>4&63],a[o+2]=i[r<<2&63],a[o+3]=61),new TextDecoder("ascii").decode(a)};
    var xhr = new XMLHttpRequest();
    xhr.responseType = 'arraybuffer';
    xhr.onload = function(){ callback(toBase64(xhr.response)) };
    xhr.onerror = function(){ callback(xhr.status) };
    xhr.open('GET', uri);
    xhr.send();
    """, uri)
    if type(result) == int:
        raise Exception("Request failed with status %s" % result)
    return base64.b64decode(result)

url_suffix = "test-"
if getattr(config, 'ENV', None) and config.ENV.lower() in [u"prod", u"production"]:
    url_suffix = ""
filename = ""
url_selenium = ""
url = ""
chrome_options = webdriver.ChromeOptions()
prefs = {
    # "download.prompt_for_download": True,
    # 'download.default_directory': os.getcwd(),
    # "plugins.always_open_pdf_externally": True,
    # 'profile.default_content_settings.popups': 0,  # 设置为0，禁止弹出窗口
}
chrome_options.add_experimental_option('prefs', prefs)
driver = webdriver.Remote(command_executor=url_selenium, desired_capabilities=chrome_options.to_capabilities())
driver.get(url_report)
now_time = time.time()
while True:
    if time.time() - now_time > 10: break
    try:
	element = driver.find_element_by_id("")
	filename = element.get_attribute("")
	element.click()
	break
    except WebDriverException:
	time.sleep(1)
now_time = time.time()
while True:
    if time.time() - now_time > 10: break
    try:
	driver.switch_to.window(driver.window_handles[-1])
	break
    except WebDriverException:
	time.sleep(1)
now_time = time.time()
while True:
    if time.time() - now_time > 60: break
    try:
	element = driver.find_element_by_xpath('//*[@id=""]')
	driver.get(element.get_property("src"))
	driver.get_screenshot_as_file("img1.png")
	break
    except WebDriverException:
	time.sleep(2)
rep_bytes = get_file_content_chrome(driver, driver.current_url)
driver.close()
driver.quit()
return rep_bytes, 200, {'Content-Type': "application/pdf",
                                   "Content-Disposition": f"attachment;filename*=UTF-8''{quote(filename)}.pdf"}
