���߳�
import threading
def climb_content(a, b):
    print 'content'


def climb_info(a, b):
    print 'info'


if __name__ == "__main__":  # ���Ժ���
    threads = []
    conn = 1
    cur = 2
    threads.append(threading.Thread(target=climb_content, args=(conn, cur)))
    threads.append(threading.Thread(target=climb_info, args=(conn, cur)))
    for t in threads:
        t.setDaemon(True)
        t.start()  # t.join()���ܷ��⣬�������̱߳���������һ���̵߳Ŀ�ʼ��������̱߳�������߳����ñ�ʧЧ
    for p in threads: 
        p.join()  # join()�����������߳�
    print threading.currentThread().name


�̳߳�
from multiprocessing.pool import ThreadPool
def hello(m, n, o):  
    print "m = %s, n = %s, o = %s"%(m, n, o)  
   
if __name__ == '__main__':  
       
   # ����1    
    lst_vars_1 = ['1', '2', '3']  
    lst_vars_2 = ['4', '5', '6']  
    func_var = [(lst_vars_1, None), (lst_vars_2, None)]  
    # ����2  
    dict_vars_1 = {'m':'1', 'n':'2', 'o':'3'}  
    dict_vars_2 = {'m':'4', 'n':'5', 'o':'6'}  
    func_var = [(None, dict_vars_1), (None, dict_vars_2)]      
       
    pool = threadpool.ThreadPool(2)  
    requests = threadpool.makeRequests(hello, func_var)  
    [pool.putRequest(req) for req in requests]
    pool.wait()

�߳���
import time, threading

# �ٶ�����������д��:
balance = 0
lock = threading.Lock()

def change_it(n):
    # �ȴ��ȡ�����Ӧ��Ϊ0:
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