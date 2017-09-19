多线程
import threading
def climb_content(a, b):
    print 'content'


def climb_info(a, b):
    print 'info'


if __name__ == "__main__":  # 测试函数
    threads = []
    conn = 1
    cur = 2
    threads.append(threading.Thread(target=climb_content, args=(conn, cur)))
    threads.append(threading.Thread(target=climb_info, args=(conn, cur)))
    for t in threads:
        t.setDaemon(True)
        t.start()  # t.join()不能放这，否则主线程被阻塞后，下一次线程的开始必须等主线程被激活，多线程作用便失效
    for p in threads: 
        p.join()  # join()用来阻塞主线程
    print threading.currentThread().name


线程池
from multiprocessing.pool import ThreadPool
def hello(m, n, o):  
    print "m = %s, n = %s, o = %s"%(m, n, o)  
   
if __name__ == '__main__':  
       
   # 方法1    
    lst_vars_1 = ['1', '2', '3']  
    lst_vars_2 = ['4', '5', '6']  
    func_var = [(lst_vars_1, None), (lst_vars_2, None)]  
    # 方法2  
    dict_vars_1 = {'m':'1', 'n':'2', 'o':'3'}  
    dict_vars_2 = {'m':'4', 'n':'5', 'o':'6'}  
    func_var = [(None, dict_vars_1), (None, dict_vars_2)]      
       
    pool = threadpool.ThreadPool(2)  
    requests = threadpool.makeRequests(hello, func_var)  
    [pool.putRequest(req) for req in requests]
    pool.wait()

线程锁
import time, threading

# 假定这是你的银行存款:
balance = 0
lock = threading.Lock()

def change_it(n):
    # 先存后取，结果应该为0:
    global balance
    balance = balance + n
    balance = balance - n

def run_thread(n):
    lock.acquire()
    for i in range(100000):
        try:
	    change_it(n)
	finally:
	    lock.release()
t1 = threading.Thread(target=run_thread, args=(5,))
t2 = threading.Thread(target=run_thread, args=(8,))
t1.start()
t2.start()
t1.join()
t2.join()
print(balance)