# -*- coding: utf8 -*-
import re
import json
import time
import errno
import urllib
import socket
import signal
import chardet
import logging


class MyAPI:
    def __init__(self, logfilename=u"", host=u"", port=20017):
        self.now_time = time.strftime(u'%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.logfilename = logfilename
        self.HOST = host
        self.PORT = port
        self.runflag = True
        self.lisfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.main()

    @staticmethod
    def initlogging(logfilename):
        logging.basicConfig(
            level=logging.DEBUG,
            # format='LINE %(lineno)-4d  %(levelname)-8s %(message)s',
            format=u'%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
            datefmt=u'%m-%d %H:%M',
            filename=logfilename,
            filemode=u'w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        # set a format which is simpler for console use
        formatter = logging.Formatter(u'%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        
    @staticmethod
    def httpresponse(header, whtml):
        context = u''.join(whtml)
        response = u"%s %d\n\n%s\n\n" % (header, len(context), context)
        return response

    @staticmethod
    def handle_post(data):
        post_data = re.findall(u"urlencoded(.*)", data, re.S)[0].strip().replace(u"&", u"\",\"").replace(u"=", u"\":\"")
        return u"{\"" + post_data + u"\"}"
    
    def siginthander(self):
        # print 'get signo# ', signo
        self.runflag = False
        self.lisfd.shutdown(socket.SHUT_RD)

    def main(self):
        httpheader = u'''
            HTTP/1.1 200 OK
            Context-Type: text/html
            Server: Python-slp version 1.0
            Context-Length: '''
        lisfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lisfd.bind((self.HOST, self.PORT))
        lisfd.listen(2)
        signal.signal(signal.SIGINT, self.siginthander)
        while self.runflag:
            try:
                confd, addr = lisfd.accept()
            except socket.error as e:
                if e.errno == errno.EINTR:
                    logging.info(u'get a except EINTR')
                else:
                    raise
                continue
            if self.runflag is False:
                break
            data = confd.recv(1024)
            if not data:
                break
            try:
                if u"/favicon.ico HTTP/1.1" in data.decode(chardet.detect(data)[u"encoding"]):  # 不判断会重复请求图标
                    continue
                jsondata_str = u""
                if re.match(u"GET", data):
                    global jsondata_str
                    jsondata_str = re.findall(u"/interface/ChangeJsonData=(.*)\s*HTTP", data)[0]
                    jsondata_str = urllib.unquote(jsondata_str)
                else:
                    global jsondata_str
                    jsondata_str = self.handle_post(data)
                logging.info(data.strip() + u"\n" + unicode(json.loads(jsondata_str)) + u"\n")
                # GetBehindData(u"getbehinddata.log", 1, jsondata_str)
                confd.send(self.httpresponse(httpheader, u'''JsonData is OK'''))
            except(IndexError, ValueError, UnicodeDecodeError, TypeError):
                confd.send(self.httpresponse(httpheader, u'''JsonData is Error'''))
                logging.info(u"json format is error")
                continue
            confd.close()
        else:
            print 'runflag#', self.runflag
        
if __name__ == u"__main__":  #
    MyAPI(u"myapi.log", u"192.168.21.17", 20017)  #
    # try:
    # print json.loads(urllib.unquote(jsondata))
    # {"docid":"", "platname":"", "msgtext":"", "pre_is_neg":"", "is_neg":"", "is_change":"", "is_resend":""}
    # GetBehindData(u"getbehinddata.log", 1, urllib.unquote(jsondata))
    #     confd.send(httpresponse(httpheader, u'''<html>
    #              <head>
    #                  <title>Emotion API</title>
    #              </head>
    #              <body>
    #                 <h1>JsonData is OK</h1>
    #              </body>
    #             </html>  '''))
    # except ValueError:
    #     confd.send(httpresponse(httpheader, u'''<html>
    #              <head>
    #                  <title>Emotion API</title>
    #              </head>
    #              <body>
    #                 <h1>JsonData is Error</h1>
    #              </body>
    #             </html>  '''))
