virtualenv
pip install virtualenv
virtualenv --no-site-packages venv (--system-site-packages)
source venv/bin/activate
deactivate

pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:8080 wsgi:application

Flask与gunicorn通信原理https://zhuanlan.zhihu.com/p/24650254
Flask 阻塞与非阻塞
https://www.jianshu.com/p/0a55507f9d9e?open_source=weibo_search
print requests.post(u"http://127.0.0.1:8000/shuju/caculate/detail", data=json.dumps({u'plat_id': u"1121", u'start_date': u"2018-02-02", u'end_date': u"2018-02-02"})).text

https:
from werkzeug.serving import make_ssl_devcert
make_ssl_devcert("server", "localhost")

Windows下:Flask是阻塞的，起用多线程依然无效(发现app.run('', port=5200, debug=False, threaded=True)可实现异步)，多进程不支持

requests:data,json default value is None.
http重定向会将post默认设为get(且不会带上参数),Flask会将参数值非None的设为'',当参数为json时会出现解析失败.
now,use requests lib request Flask1.0.2 in python2.7(params {'a':1}):
is_data>is_redirect>is_jsondumps
get_json():
  -data
    no support,None
  -json
    -redirect
      -jsondumps
        unicode:u'{"a": 1}'>str:'',return 400 Failed to decode JOSN object
      -no jsondumps
        dict:{u'a': 1}>str:'',return 400 Failed to decode JOSN object
    -no redirect
      -jsondumps
        unicode:u'{"a": 1}'
      -no jsondumps
        dict:{u'a': 1}

get_data():
  -data
    -redirect
      -jsondumps
        str:'{"a": 1}'>str:''
      -no jsondumps
        str:'a=1'>str:''
    -no redirect
      -jsondumps
        str:'{"a": 1}'
      -no jsondumps
        str:'a=1'
  -json
    -redirect
      -jsondumps
        str:'"{\\"a\\": 1}"'>str:'',return 400 Failed to decode JOSN object
      -no jsondumps
        str:'{"a": 1}'>str:'',return 400 Failed to decode JOSN object
    -no redirect
      -jsondumps
        str:'"{\\"a\\": 1}"'
      -no jsondumps
        str:'{"a": 1}'
      
form:
  -data
    -redirect
      -jsondumps
        ImmutableMultiDict([])>ImmutableMultiDict([])
      -no jsondumps
        ImmutableMultiDict([('a', u'1')]))>ImmutableMultiDict([])
    -no redirect
      -jsondumps
        ImmutableMultiDict([])
      -no jsondumps
        ImmutableMultiDict([('a', u'1')]))
  -json
    -redirect
      -jsondumps
        ImmutableMultiDict([])>ImmutableMultiDict([])
      -no jsondumps
        ImmutableMultiDict([('a', u'1')]))>ImmutableMultiDict([])
    -no redirect
      -jsondumps
        ImmutableMultiDict([])
      -no jsondumps
        ImmutableMultiDict([])
