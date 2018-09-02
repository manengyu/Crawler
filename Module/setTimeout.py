# -*- coding: utf-8 -*-
# only support Unix-like system
import time
import signal

class TimeOutException(Exception):
    pass

def setTimeout(num, callback):
    def wrapper(func):
        def handle(signum, frame):
            raise TimeOutException(u"运行超时！")
        def toDo(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handle)
                signal.alarm(num)  # 开启闹钟信号
                rs = func(*args, **kwargs)
                signal.alarm(0)  # 关闭闹钟信号
                return rs
            except TimeOutException, e:
                callback(args[0])
        return toDo
    return wrapper

def doSome(args):
    print u"timeout", args

@setTimeout(4,doSome)
def handle_business(name, pwd):
    time.sleep(6)
    return name,pwd

rnt_data = handle_business(u"1", u"2")
if rnt_data:
    print(u"success", rnt_data)  # (u'success', (u'1', u'2'))
else:
    print(u"fail,timeout")  # timeout 1

