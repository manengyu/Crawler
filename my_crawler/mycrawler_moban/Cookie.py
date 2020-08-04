//JSESSIONID一般在获取验证码图片中返回

import time
from hashlib import md5
from random import randint


tmp = ""
uid = str(randint(0, 255))
m1 = md5()
m1.update(uid.encode())
uid = m1.hexdigest()
Degrees.cookie["JSESSIONID"] = uid.upper()
Degrees.cookie["Hm_lvt_"] = str(int(time.time()))
Degrees.cookie["Hm_lpvt_"] = str(int(time.time()))
for k, v in A.items():
    tmp += f"{k}={v};"
tmp.strip(";")
reqs.headers["cookie"] = tmp
