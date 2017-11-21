# -*- coding: utf8 -*-
from functools import wraps
from flask import Flask, make_response
# from flask_script import Manager
import sys
import time
import socket
import platform
from multiprocessing import Process, Queue
import subprocess


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


app = Flask(__name__)
some_queue = Queue()


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
    try:
        print 0
    except:
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


def get_ip():
    if platform.system() == u'Windows':
        hostname = socket.gethostname()
        inip = socket.gethostbyname_ex(hostname)[-1][-1]
    else:
        import fcntl
        import struct
        sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # outip = socket.inet_ntoa(fcntl.ioctl(sk.fileno(), 0x8915, struct.pack('256s', "lo"[:15]))[20:24])
        inip = socket.inet_ntoa(fcntl.ioctl(sk.fileno(), 0x8915, struct.pack('256s', "eth0"[:15]))[20:24])
    return inip


def start_flaskapp(queue):
    global some_queue
    some_queue = queue
    ip = get_ip()
    app.run(host=ip, port=20018, debug=False, threaded=True)


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
