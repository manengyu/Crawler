# -*- coding: utf8 -*-
import sys
import time
import socket
import platform
import subprocess
from functools import wraps
# from flask_script import Manager
from werkzeug.routing import Rule
from flask import Flask, make_response
from multiprocessing import Process, Queue


def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers[u'Access-Control-Allow-Origin'] = u'*'
        rst.headers[u'Access-Control-Allow-Methods'] = u'PUT,GET,POST,DELETE'
        allow_headers = u"Referer,Accept,Origin,User-Agent"
        rst.headers[u'Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun


class CIRule(Rule):
    def compile(self):
        Rule.compile(self)  # 设置不加/，实际匹配有无/都可匹配到
        self._regex = re.compile(re.sub(u"([^)])\$", u"\g<1>/?$", self._regex.pattern),  # 忽略url中大小写
                                 re.UNICODE | re.IGNORECASE)
        print self._regex.pattern


class CIFlask(Flask):
    url_rule_class = CIRule


app = CIFlask(__name__)


@app.before_request
def before_request():
    # 可检查权限
    pass
some_queue = Queue()


def respose_json(data, status):
    if status == 200 or status == 204:
        pass
    elif status == 500:
        data = {u"timestamp": int(time.time()), u"status": status, u"message": data, u"path": u"/",
                u"error": u"Internal Server Error"}
    else:
        data = {u"timestamp": int(time.time()), u"status": status, u"message": data, u"path": u"/",
                u"error": u"Bad Request"}
    ret_data = json.dumps(data, ensure_ascii=False)
    # if status == 500 or status == 408 or status == 204 or status == 400:
    # else:
    return ret_data


@app.route(u'/post', methods=[u'POST'])  # 创建运营人员
@allow_cross_domain
def post_request():
    pass


@app.route(u'/api/update', methods=[u'POST', u'GET'])
@allow_cross_domain
def doc_sent_score():
    # from flask import request
    # request.method = u"POST":
    # try:
    #     title = request.form.get(u"title")
    # except Exception as e:
    #     status = False
    #     msg = u'Failed to parse'
    #     print(u"data failed to parse with the reason", e)
    #  request.method = u"GET":
    # request.args.get()
    try:
        print 0
    except RuntimeError:
        return u"operate error"
    return u"operate ok"


@app.route(u'/api/reload', methods=[u'POST', u'GET'])
def restart():
    try:
        some_queue.put()
        print(u"Restarted successfully")
        return u"Successfully"
    except TypeError:
        print(u"Failed in restart")
        return u"Failed"


def get_ip(net_card=u"eth0"):
    if platform.system() == u'Windows':
        hostname = socket.gethostname()
        inip = socket.gethostbyname_ex(hostname)[-1][-1]
    else:
        import fcntl
        import struct
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # outip = socket.inet_ntoa(fcntl.ioctl(sk.fileno(), 0x8915, struct.pack('256s', "lo"[:15]))[20:24])
        inip = socket.inet_ntoa(
            fcntl.ioctl(sk.fileno(), 0x8915, struct.pack(  # pack only accepts bytes
                u'256s'.encode(u"utf-8"), unicode(net_card[:15]).encode(u"utf-8")))[20:24])  # 2unicode,3str
    return inip


def start_flaskapp(queue):
    global some_queue
    some_queue = queue
    ip = get_ip()
    app.run(host=ip, port=20018, debug=False, threaded=True)

    # from gevent.wsgi import WSGIServer
    # http_server = WSGIServer(app, host=ip, port=20019)
    # http_server.serve_forever()

    # import wsgiserver
    # server = wsgiserver.WSGIServer(app, host=ip, port=20019)
    # server.start()


def main():
    q = Queue()
    p = Process(target=start_flaskapp, args=[q, ])
    p.start()
    while True:  # wathing queue, if there is no call than sleep, otherwise break
        if q.empty():
            time.sleep(1)
        else:
            break
    p.terminate()  # terminate flaskapp and then restart the app on subprocess
    args = [sys.executable] + [sys.argv[0]]
    subprocess.call(args)


if __name__ == u'__main__':
    main()
