# _*_ coding: utf-8 _*_

import re
import rsa
import time
import json
import base64
import logging
import binascii
import requests
import urllib
import random
from PIL import Image
import cookielib


class WeiBoLogin(object):
    """
    class of WeiBoLogin, to login weibo.py.com
    """

    def __init__(self):
        """
        constructor
        """
        self.user_name = None
        self.pass_word = None
        self.user_uniqueid = None
        self.user_nick = None

        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0"})
        # self.session.proxies = self.get_proxies()
        # self.session.cookies = self.get_cookies()
        # print {c.name: c.value for c in self.get_cookies()}
        self.session.get("http://weibo.py.com/login.php")
        return

    def login(self, user_name, pass_word):
        """
        login weibo.py.com, return True or False
        """
        self.user_name = user_name
        self.pass_word = pass_word
        self.user_uniqueid = None
        self.user_nick = None

        # get json data
        s_user_name = self.get_username()
        json_data = self.get_json_data(su_value=s_user_name)
        if not json_data:
            return False
        s_pass_word = self.get_password(json_data["servertime"], json_data["nonce"], json_data["pubkey"])

        # make post_data
        post_data = {
            "entry": "weibo.py",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.py.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": json_data["rsakv"],
            "servertime": json_data["servertime"],
            "nonce": json_data["nonce"],
            "su": s_user_name,
            "sp": s_pass_word,
            "returntype": "TEXT",
        }

        # get captcha code
        if json_data["showpin"] == 1:
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), json_data["pcid"])
            with open("captcha.gif", "wb") as file_out:  # captcha.jpeg
                file_out.write(self.session.get(url).content)
            code = input("请输入验证码:")
            # with open('image/captcha.gif', 'wb') as f:
            #     f.write(r.content)
            # image = Image.open('captcha.gif')
            # code = ''
            # try:
            #     code = pytesseract.image_to_string(image, lang='eng')
            # except Exception:
            #     pass
            # print code
            post_data["pcid"] = json_data["pcid"]
            post_data["door"] = code

        # login weibo.py.com
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())
        json_data_1 = self.session.post(login_url_1, data=post_data).json()
        if json_data_1["retcode"] == "0":
            params = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "client": "ssologin.js(v1.4.18)",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "_": int(time.time()*1000),
            }
            response = self.session.get("https://passport.weibo.py.com/wbsso/login", params=params)
            json_data_2 = json.loads(re.search(r"\((?P<result>.*)\)", response.text).group("result"))
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                logging.warning("WeiBoLogin succeed: %s", json_data_2)
                # print type(response.cookies), response.cookies
                # print {c.name: c.value for c in response.cookies}
                # new_cookie_jar = cookielib.LWPCookieJar("./my" + '.txt')
                #
                # # 将转换成字典格式的RequestsCookieJar（这里我用字典推导手动转的）保存到LWPcookiejar中
                # requests.utils.cookiejar_from_dict({c.name: c.value for c in self.session.cookies}, new_cookie_jar)
                #
                # # 保存到本地文件
                # new_cookie_jar.save('./my' + '.txt', ignore_discard=True, ignore_expires=True)
            else:
                logging.warning("WeiBoLogin failed: %s", json_data_2)
        else:
            logging.warning("WeiBoLogin failed: %s", json_data_1)
        return True if self.user_uniqueid and self.user_nick else False

    def get_username(self):
        """
        get legal username
        """
        username_quote = urllib.quote(self.user_name)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    def get_json_data(self, su_value):
        """
        get the value of "servertime", "nonce", "pubkey", "rsakv" and "showpin", etc
        """
        params = {
            "entry": "weibo.py",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "su": su_value,
            "_": int(time.time()*1000),
        }
        try:
            response = self.session.get("http://login.sina.com.cn/sso/prelogin.php", params=params)
            json_data = json.loads(re.search(r"\((?P<data>.*)\)", response.text).group("data"))
        except Exception as excep:
            json_data = {}
            logging.error("WeiBoLogin get_json_data error: %s", excep)

        logging.debug("WeiBoLogin get_json_data: %s", json_data)
        return json_data

    def get_password(self, servertime, nonce, pubkey):
        """
        get legal password
        """
        string = (str(servertime) + "\t" + str(nonce) + "\n" + str(self.pass_word)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        password = binascii.b2a_hex(password)
        return password.decode()

    def get_content(self, url):
        response = self.session.get(url)
        # print response.content
        return response.content

    # def get_location(self, url):
    #     return self.session.get(url).content
    def get_proxies(self):
        ip = json.loads(requests.get(
                "http://dps.kuaidaili.com/api/getdps/?orderid=958964320330191&num=50&ut=1&format=json&sep=1").content)
        print ip
        proxies = {
            "http": "http://8283891:ojonvhe8@" + ip["data"]["proxy_list"][random.randint(0, len(ip)-1)]
        }
        return proxies

    def get_cookies(self):
        # return "<RequestsCookieJar[<Cookie SRF=1497867826 for .passport.weibo.py.com/>, <Cookie SRT=D.QqHBJZ4n4ObTJrMbP" \
        #        "FYGS4uGiDEPdZY9U!su5cbHNEYddmyPAsypMERt4EPKRcsrA4uJ4!olTsVtUGbROQ!sKmYlJ4iuT4rnA!iFNFyoMqMjOmPeI8t7" \
        #        "*B.vAflW-P9Rc0lR-ykTDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPVsSsHdW8sFWO4pWZE4UqmpS-joUZHwi49n" \
        #        "dDPIJcYPSrnlMc0k4ZEfOPHbUrr3SdYCJcM1OFyHi3!nN4WJU-P6iQBOUeMr for .passport.weibo.py.com/>, <Cookie SC" \
        #        "F=AvWBUbNx6USWjQ3QfYQKQuL5LkjhSzxD-eiKR0LcNLS1bapc8gFrYZUi8_IQVBqj92EE0HmmyU0g6nOVu3tkRtQ. for ." \
        #        "weibo.py.com/>, <Cookie SSOLoginState=1497867826 for .weibo.py.com/>, <Cookie SUB=_2A250Q9Z3DeThGeNG41UZ" \
        #        "8inMyziIHXVXOUC_rDV8PUNbmtANLRLnkW8lyXMy58Hn1CyiM0BCFHoqG4lLEg.. for .weibo.py.com/>, <Cookie SUBP=0033" \
        #        "WrSXqPxfM725Ws9jqgMF55529P9D9W5gRVv-Fu52v1To12gk1n2z5JpX5K2hUgL.Fo-R1hMReoM7ehB2dJLoI7y0IGLoeo5pSntt" \
        #        " for .weibo.py.com/>, <Cookie SUHB=0D-VpUXPeBscqU for .weibo.py.com/>]>"
        # return {'SUHB': '0vJYHNRI3PWjSR',
        #         'SRF': '1497923374',
        #         'SUB': '_2A250TA9-DeThGeNG41UZ8inMyziIHXVXOGe2rDV8PUNbmtANLUfVkW8kaEf1K8IAL_MOFolfpq1-oaJ6qQ..',
        #         'SUBP': '0033WrSXqPxfM725Ws9jqgMF55529P9D9W5gRVv-Fu52v1To12gk1n2z5JpX5K2hUgL.Fo-R1hMReoM7ehB2dJLoI7y0IGLoeo5pSntt',
        #         'SCF': 'AvWBUbNx6USWjQ3QfYQKQuL5LkjhSzxD-eiKR0LcNLS1NeLghK9NRQptpYOc6AmYKK3h7VtUNESR-LjA3ec_Aas.',
        #         'SRT': 'D.QqHBJZ4nPmmuI4MbPFYGS4uGiDEPdZY9U!su5cbHNEYddmyGSOHpMERt4EPKRcsrA42017-06-20 09:49:29,788	DEBUG	Starting new HTTP connection (1): 115.159.99.103\
        #         uJPdSdTsVtT-EESZEIKmbBOEyiOrS6UFSnVOmkU-E1ieEMI8t7*B.vAflW-P9Rc0lR-ykTDvnJqiQVbiRVPBtS!r3JZPQVqbgVdWiMZ4siOzu4DbmKPVsSsHdW8sFWO4pWZE4UqmpS-joUZHwi49ndDPIJcYPSrnlMc0k4ZEfOPHbUrr3SdYCJcM1OFyHi3!nN4WJU-P6iQBOUeMr',
        #         'SSOLoginState': '1497923374'}
        # 实例化一个LWPCookieJar对象
        load_cookiejar = cookielib.LWPCookieJar()
        # 从文件中加载cookies(LWP格式)
        load_cookiejar.load('./my' + '.txt', ignore_discard=True, ignore_expires=True)
        # 工具方法转换成字典
        load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)
        # 工具方法将字典转换成RequestsCookieJar，赋值给session的cookies.
        return requests.utils.cookiejar_from_dict(load_cookies)


def login(url):
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
    weibo = WeiBoLogin()
    weibo.login("wdzj_wb@163.com", "wdzj2016")
    return weibo.get_content(url), weibo


# def login_wap(url):
#     logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
#     weibo.py = WeiBoLogin()
#     weibo.py.login("wdzj_wb@163.com", "wdzj2016")
#     return weibo.py.get_location(url)
