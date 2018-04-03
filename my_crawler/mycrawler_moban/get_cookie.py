# -*- coding: utf8 -*-
""""
when using cookie，sure to add User-Agent
for example:
Windows-Chrome:
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36
Linux-Firefox:Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Max-Firefox:Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:54.0) Gecko/20100101 Firefox/54.0

suggest:
Linux: use Firefox, and add PATH=$PATH:geckodriver_path to command when using crontab
"""
import time
from selenium import webdriver
from pyvirtualdisplay import Display


class GetCookie:
    def __init__(self, url, ):
        self.cookie = u""
        self.br = u""
        self.main(url)
        
    def login(self):
        element = self.br.find_element_by_xpath(u"//div[@class='']/input").send_keys(u"")
        element = self.br.find_element_by_xpath(u"//div[@class='']/input").send_keys(u"")
        element = self.br.find_element_by_xpath(u"//div[@class='']/input")
        element.click()
        # action = ActionChains(self.br)
        # action.click(element).perform()
        js = u"""document.querySelectorAll('[change-type=""]')[0].getElementsByClassName('')[0].
        getElementsByTagName('')[0].click();"""
        
    def main(self, url):
        display = Display(visible=0, size=(800, 600))
        display.start()  # no gui
        self.br = webdriver.Firefox()  # .Chrome()  sure to geckodriver or chromedriver.exe in PATH
        # Ie('C:\Program Files (x86)\Internet Explorer\IEDriverServer.exe')
        self.br.get(url)
        time.sleep(10)  # if time is short,cookie may be lost
        cookie = [item[u"name"] + u"=" + item[u"value"] for item in br.get_cookies()]
        self.cookie = u';'.join(item for item in cookie)
        self.br.close()
        display.stop()
        
    def get_cookie(self):
        return self.cookie
