virtualenv
pip install virtualenv
virtualenv --no-site-packages venv (--system-site-packages)
source venv/bin/activate
deactivate

pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:8080 wsgi:application

Flask��gunicornͨ��ԭ��https://zhuanlan.zhihu.com/p/24650254
Flask �����������
https://www.jianshu.com/p/0a55507f9d9e?open_source=weibo_search
print requests.post(u"http://127.0.0.1:8000/shuju/caculate/detail", data=json.dumps({u'plat_id': u"1121", u'start_date': u"2018-02-02", u'end_date': u"2018-02-02"})).text

Windows��:Flask�������ģ����ö��߳���Ȼ��Ч(����app.run('', port=5200, debug=False, threaded=True)��ʵ���첽)������̲�֧��