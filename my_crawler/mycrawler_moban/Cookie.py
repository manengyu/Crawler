//JSESSIONID一般在获取验证码图片中返回

import time
from hashlib import md5
from random import randint


tmp = ""
cookie = ""
uid = str(randint(0, 255))
m1 = md5()
m1.update(uid.encode())
uid = m1.hexdigest()
cookie["JSESSIONID"] = uid.upper()
cookie["Hm_lvt_"] = str(int(time.time()))
cookie["Hm_lpvt_"] = str(int(time.time()))
for k, v in A.items():
    tmp += f"{k}={v};"
tmp = tmp.strip(";")
//cannot use reqs.headers = headers
r = reqs.get(url, headers={"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                            "Accept-Encoding":"gzip, deflate",
                            "Accept-Language":"zh-CN,zh;q=0.9",
                            "Cache-Control":"max-age=0",
                            "Content-Length":"227",
                            "Content-Type":"application/x-www-form-urlencoded",
                            "Host":"",
                            "Origin":"",
                            # "Proxy-Connection":"keep-alive",
                            "Connection":"keep-alive",
                            "Referer":"",
                            "Upgrade-Insecure-Requests":"1",
                            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                            "cookie": tmp,
                            })


# handle browser cookie
# # aa = {}
a = ""
rtn = ''
a = a.replace(" ", "").replace(" ", "")
for i in a.split(";"):
    rtn += f'document.cookie="{i.strip()}";'
#     print(i)
#     ii = i.split("=")
#     aa[ii[0]] = ii[1]
# import json
print(rtn)
# print(json.dumps(aa))
