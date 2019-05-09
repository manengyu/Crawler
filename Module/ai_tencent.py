import time
import json
import random
import requests


def genSignString(parser):
    import hashlib
    from urllib import parse
    uri_str = ''
    for key in sorted(parser.keys()):
        if key == 'app_key':
            continue
        uri_str += "%s=%s&" % (key, parse.quote(str(parser[key]), safe=''))
    sign_str = uri_str + 'app_key=' + parser['app_key']

    hash_md5 = hashlib.md5(sign_str.encode())
    return hash_md5.hexdigest().upper()


data = {}
now_time = int(time.time())
params = dict({"app_id": "",
               "app_key": "", "image": data["base64"],
               "nonce_str": f"{random.randint(0, 9)}", "time_stamp": now_time})
params["sign"] = genSignString(params)
res = requests.post("https://api.ai.qq.com/fcgi-bin/ocr/ocr_generalocr", params)
if 200 == res.status_code:
    if 0 is not json.loads(res.text)["ret"]:
        raise Exception()
    # return json.dumps(json.loads(res.text)["data"], ensure_ascii=False)
