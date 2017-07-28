# -*- coding: utf8 -*-

# import login_weibo
import MySQLdb
import pandas as pd
import threading
import requests
import urllib
import re
import traceback
import random
import datetime
import time
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


# 连接数据库
def connect_database(db_nick='yuqing'):
    if db_nick == 'zhangrz':
        try:
            conn = MySQLdb.connect(host='192.168.8.195', user='wdzj_many', passwd='wdzj_many',
                                   db='zhangrz', port=3306, charset='utf8')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    elif db_nick == 'yuqing':
        try:
            conn = MySQLdb.connect(host='192.168.11.140', user='wdzj_many', passwd='wdzj_many',
                                   db='yuqing', port=3306, charset='utf8')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    elif db_nick == 'yuqing_b':
        try:
            conn = MySQLdb.connect(host='192.168.11.140', user='wdzj_many', passwd='wdzj_many',
                                   db='yuqing_b', port=3306, charset='utf8')
        except MySQLdb.Error, e:
            print "Mysql Error %d: %s" % (e.args[0], e.args[1])
    else:
        print 'No such database!!!'
    return conn


def insert_management(conn, cur, plat_name, account_url):
    day_date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    create_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    insert_sql = "INSERT INTO yuqing.weibo_management (plat_name, account_url) VALUES ('" + str(plat_name) + "','" + str(account_url) +\
                 + "')"
    # insert_sql = "INSERT INTO yuqing.weibo_management (plat_name, account_url, use_for) VALUES ('" + str(plat_name) + "','" + str(account_url) + "','B"\
    #              + "')"
    # select_sql = "SELECT * FROM yuqing.weibo_info"
    # app_management = pd.read_sql(select_sql, conn)
    # if account_id not in list(app_management.get("account_id")):
        # print account_id, level, follow_count, followers_count, wb_count, day_date, create_time
    cur.execute(insert_sql)
    conn.commit()


def update_managerment(conn, cur, account, account_id,  verified, description, account_url):
    update_sql = "UPDATE yuqing.weibo_management SET weibo_account='" + account + "', account_id='" + account_id  + "' , verified='"\
                 + verified + "' , description='" + description + "' where account_url='" + account_url + "'"
    cur.execute(update_sql)
    conn.commit()


def insert_info(conn, cur, account_id, level, follow_count, followers_count, wb_count):
    day_date = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    create_time = str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    insert_sql = "INSERT INTO yuqing.weibo_info (account_id, level, follow_count, followers_count, wb_count, day_date, create_time) VALUES ('" + str(account_id) + "','" +str(level) + "','" \
                 + str(follow_count) + "','" + str(followers_count) + "','" + str(wb_count) + "','" + \
                 day_date + "','" + \
                 create_time + \
                 "')"
    # select_sql = "SELECT * FROM yuqing.weibo_info"
    # app_management = pd.read_sql(select_sql, conn)
    # if account_id not in list(app_management.get("account_id")):
        # print account_id, level, follow_count, followers_count, wb_count, day_date, create_time
    try:
        cur.execute(insert_sql)
        conn.commit()
    except:
        traceback.print_exc()
        pass


def insert_content(conn, cur, account_id, weibo_id, source, content, comments_count,
                           like_count, reposts_count, repost_from, repost_content, pub_date, weibo_url, weibo_account):
    insert_sql = "INSERT INTO yuqing.weibo_content (account_id, weibo_id, source, content, comments_count, " \
                 "like_count, reposts_count, repost_from, repost_content, pub_date, weibo_url, weibo_account, docid) VALUES ('" + \
                 account_id + "','" + weibo_id + "','" + source + "','" + content + "','" + comments_count + "','" + \
                 like_count + "','" + reposts_count + "','" + repost_from + "','" + repost_content + "','" + \
                 pub_date + "','" + weibo_url + "','" + weibo_account + "', UPPER(replace(UUID(),\'-\',\'\')))"
    select_sql = "SELECT * FROM yuqing.weibo_content"
    app_management = pd.read_sql(select_sql, conn)
    if weibo_id not in list(app_management.get("weibo_id")):
        # print account_id, weibo_id, source, content, comments_count, like_count, reposts_count, repost_from, repost_content, pub_date, weibo_url
        try:
            cur.execute(insert_sql)
            conn.commit()
        except:
            traceback.print_exc()
            pass


def insert_content_b(account_id, weibo_id, source, content, comments_count,
                       like_count, reposts_count, repost_from, repost_content, pub_date, weibo_url, weibo_account):
    conn_yuqing_b = connect_database(db_nick='yuqing_b')
    cur_b = conn_yuqing_b.cursor()
    insert_sql = "INSERT INTO yuqing_b.weibo_content (account_id, weibo_id, source, content, comments_count, " \
                 "like_count, reposts_count, repost_from, repost_content, pub_date, weibo_url,weibo_account, docid) VALUES ('" + \
                 account_id + "','" + weibo_id + "','" + source + "','" + content + "','" + comments_count + "','" + \
                 like_count + "','" + reposts_count + "','" + repost_from + "','" + repost_content + "','" + \
                 pub_date + "','" + weibo_url + "','" + weibo_account + "', UPPER(replace(UUID(),\'-\',\'\')))"
    try:
        cur_b.execute(insert_sql)
        conn_yuqing_b.commit()
    except:
        traceback.print_exc()
        pass


def get_weibo_management(page_id, r):
    user_info = json.loads(r.get("https://m.weibo.cn/api/container/getIndex?containerid=" + page_id).content)
    account = user_info["userInfo"]["screen_name"]
    verified = ""
    description = ""
    if "verified_reason" in user_info["userInfo"].keys():
        verified = user_info["userInfo"]["verified_reason"]
    if "description" in user_info["userInfo"].keys():
        description = user_info["userInfo"]["description"]
    print account, verified, description
    return account, verified, description


def get_weibo_info(account_id, page_id, r):
    try:
        user_info = json.loads(r.get("https://m.weibo.cn/api/container/getIndex?containerid=" + page_id).content)
    except:
        print "https://m.weibo.cn/api/container/getIndex?containerid=" + page_id
        print "数据格式有误"
        traceback.print_exc()
        return
    if "userInfo" in user_info.keys():
        level = user_info["userInfo"]["urank"]
        follow_count = user_info["userInfo"]["follow_count"]
        followers_count = user_info["userInfo"]["followers_count"]
        wb_count = user_info["userInfo"]["statuses_count"]
        # print account_id, level, follow_count, followers_count, wb_count
        return account_id, level, follow_count, followers_count, wb_count


def get_weibo_content(conn_yuqing, cur, account_id, page_id, r, isb):
    time.sleep(1)
    containerid = ""
    user_info = ""
    screen_name = ""
    try:
        user_info = json.loads(r.get("https://m.weibo.cn/api/container/getIndex?containerid=" + page_id).content)
        screen_name = user_info["userInfo"]["screen_name"]
    except:
        print "请求过于频繁,歇歇吧"
        return
    if "tabsInfo" not in user_info.keys():
        return
    else:
        containerid = user_info["tabsInfo"]["tabs"][1]["containerid"]
    for i in range(1, 2):  # 共爬取4页
        try:
            content_info = json.loads(r.get("https://m.weibo.cn/api/container/getIndex?containerid=" + containerid + "&page=" + str(i)).content)
        except:
            print "请求过于频繁,歇歇吧!"
            continue
        if "cards" not in content_info.keys():
            continue
        for i in content_info["cards"]:
            if "mblog" not in i.keys():
                continue
            weibo_id = i["mblog"]["id"]
            source = i["mblog"]["source"]
            content = urllib.unquote(check_illegal(urllib.unquote(i["mblog"]["text"].replace("'", "\"").encode("utf-8"))))
            comments_count = str(i["mblog"]["comments_count"])
            like_count = str(i["mblog"]["attitudes_count"])
            reposts_count = str(i["mblog"]["reposts_count"])
            repost_from = ""
            repost_content = ""
            try:
                if "retweeted_status" in i["mblog"].keys() and i["mblog"]["retweeted_status"]["user"] is not None:
                    # print type(i["mblog"]["retweeted_status"]), i["mblog"]["retweeted_status"]
                    repost_from = i["mblog"]["retweeted_status"]["user"]["screen_name"]
                    repost_content = urllib.unquote(check_illegal(urllib.unquote(i["mblog"]["retweeted_status"]["text"].replace("'", "\"").encode("utf-8"))))
                    # print check_illegal(i["mblog"]["retweeted_status"]["text"].replace("'", "\""))
                    # print repost_content + "\n"
            except:
                traceback.print_exc()
                continue
            weibo_url = "https://m.weibo.cn/status/" + weibo_id
            pub_date = handle_time(str(i["mblog"]["created_at"].strip()))
            insert_content(conn_yuqing, cur, account_id, weibo_id, source, content, comments_count,
                           like_count, reposts_count, repost_from, repost_content, pub_date, weibo_url, screen_name)
            if isb == 1:
                insert_content_b(account_id, weibo_id, source, content, comments_count,
                               like_count, reposts_count, repost_from, repost_content, pub_date, weibo_url, screen_name)


def get_url(conn):
    select_sql = "SELECT * FROM yuqing.weibo_management"
    app_management = pd.read_sql(select_sql, conn)
    ls_url = app_management.get("account_url")
    return ls_url


def check_illegal(text):
    illegal = ["😂", "🐒", "😹", "🎉", "🐔", "👉", "🐷"]
    for k in illegal:
        text = text.replace(k, "")
    return text  # .replace("😂", "").replace("🐒", "").replace("😹", "").replace("🎉", "").replace("🐔", "")
    # .replace("👉", "").replace("🐷", "")


def handle_time(mtime):
    if "今天" in mtime:
        mtime = time.strftime('%m-%d', time.localtime(time.time())) + mtime.lstrip("今天")
    if "分钟前" in mtime:
        t = time.time() - int(re.findall("(\d+)", mtime)[0]) * 60
        mtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(t))
    if len(mtime) < 13:
        mtime = str(datetime.datetime.now().year) + "-" + mtime
    return mtime


def get_proxies():
    ip = json.loads(requests.get(
            "http://dps.kuaidaili.com/api/getdps/?orderid=958964320330191&num=50&ut=1&format=json&sep=1").content)
    proxies = {  # 每次请求从代理ip中随机产生一个地址
        "http": "http://8283891:ojonvhe8@" + ip["data"]["proxy_list"][random.randint(0, len(ip)-1)]
    }
    return proxies


def climb_management(conn_yuqing, cur):
    for i in get_url(conn_yuqing):  # 爬取管理信息
    # #    con, weibo.py = login_weibo.login(i)
        r = requests.session()
        r.proxies = get_proxies()
        account_id = i.lstrip("http://m.weibo.com/u/")
        page_id = r.get(i).url.lstrip("https://m.weibo.cn/p/")
        account, verified, description = get_weibo_management(page_id, r)
        update_managerment(conn_yuqing, cur, account, account_id, verified, description, i)
    print "weibo_management climb finish"


def climb_content(conn_yuqing, cur):
    for i in get_url(conn_yuqing):  # 爬取微博内容
        # con, weibo.py = login_weibo.login(i)
        r = requests.session()
        r.proxies = get_proxies()
        account_id = i.lstrip("http://m.weibo.com/u/")
        try:
            page_id = r.get(i).url.lstrip("https://m.weibo.cn/p/")
        except:
            traceback.print_exc()
            time.sleep(1)
            continue
        if isinb(i):
            get_weibo_content(conn_yuqing, cur, account_id, page_id, r, 1)
        else:
            get_weibo_content(conn_yuqing, cur, account_id, page_id, r, 0)
        time.sleep(1)
    print "weibo_content climb finish"


def climb_info(conn_yuqing, cur):
    for i in get_url(conn_yuqing):  # 爬取微博信息
    #    con, weibo.py = login_weibo.login(i)
        r = requests.session()
        r.proxies = get_proxies()
        account_id = i.lstrip("http://m.weibo.com/u/")
        try:
            page_id = r.get(i).url.lstrip("https://m.weibo.cn/p/")
            account_id, level, follow_count, followers_count, wb_count = get_weibo_info(account_id, page_id, r)
        except:
            traceback.print_exc()
            print i
            time.sleep(1)
            continue
        insert_info(conn_yuqing, cur, account_id, level, follow_count, followers_count, wb_count)
    print "weibo_info climb finish"


def isinb(url):
    if url in ["http://m.weibo.com/u/1778181617",
        "http://m.weibo.com/u/1999861363",
        "http://m.weibo.com/u/5475745952",
        "http://m.weibo.com/u/1493100750",
        "http://m.weibo.com/u/3665284370",
        "http://m.weibo.com/u/5386376991",
        "http://m.weibo.com/u/3916154678",
        "http://m.weibo.com/u/3936065378",
        "http://m.weibo.com/u/2216400883",
        "http://m.weibo.com/u/1638782947",
        "http://m.weibo.com/u/2258727970",
        "http://m.weibo.com/u/1645611272",
        "http://m.weibo.com/u/3962947301",
        "http://m.weibo.com/u/3509086252",
        "http://m.weibo.com/u/5688133309",
        "http://m.weibo.com/u/6080278601",
        "http://m.weibo.com/u/1163218074",
        "http://m.weibo.com/u/1649252577",
        "http://m.weibo.com/u/2311077472",
        "http://m.weibo.com/u/1649173367",
        "http://m.weibo.com/u/5162765902",
        "http://m.weibo.com/u/1651428902",
        "http://m.weibo.com/u/1641561812",
        "http://m.weibo.com/u/3042972463",
        "http://m.weibo.com/u/6226682489",
        "http://m.weibo.com/u/1663937380",
        "http://m.weibo.com/u/1729503667",
        "http://m.weibo.com/u/5863639760",
        "http://m.weibo.com/u/1698233740"]:
        return True
    else:
        return False


def merge_update():
    conn_y = connect_database(db_nick='yuqing')
    select_sql = "SELECT * FROM yuqing.weibo_content"
    app_management = pd.read_sql(select_sql, conn_y)
    conn_yuqing_b = connect_database(db_nick='yuqing_b')
    cur_b = conn_yuqing_b.cursor()
    for i in range(0, app_management.shape[0]):  # 合并content\
        mtime = app_management.irow(i)["pub_date"]
        weibo_url = "https://m.weibo.cn/status/" + str(app_management.irow(i)["weibo_id"])
        insert_sql = "INSERT INTO yuqing_b.weibo_content (account_id, weibo_id, source, content, comments_count, " \
                     "like_count, reposts_count, repost_from, repost_content, pub_date, weibo_url, docid) VALUES ('" + \
                     app_management.irow(i)["account_id"] + "','" + app_management.irow(i)["weibo_id"] + "','" + \
                     app_management.irow(i)["source"] + "','" + app_management.irow(i)["content"] + "','" + str(
            app_management.irow(i)["comments_count"]) + "','" + \
                     str(app_management.irow(i)["like_count"]) + "','" + str(
            app_management.irow(i)["reposts_count"]) + "','" + str(app_management.irow(i)["repost_from"]) + "','" + \
                     app_management.irow(i)["repost_content"] + "','" + \
                     mtime + "','" + weibo_url + "', '" + str(app_management.irow(i)["docid"]) + "')"
        cur_b.execute(insert_sql)
        conn_yuqing_b.commit()


def update_weibo_account(conn, cur):  # 新增微博帐号
    conn_yuqing_b = connect_database(db_nick='yuqing_b')
    cur_b = conn_yuqing_b.cursor()
    select_sql = "SELECT * FROM yuqing.weibo_content"
    app_management = pd.read_sql(select_sql, conn)
    for i in  app_management.iterrows():
        update_sql = "UPDATE yuqing.weibo_content SET repost_content='" + urllib.unquote(urllib.unquote(i[1]["repost_content"])) + \
                     "' where docid='" + i[1]["docid"] + "'"
        cur.execute(update_sql)
        conn_yuqing.commit()
    select_sql_b = "SELECT * FROM yuqing_b.weibo_content"
    app_management_b = pd.read_sql(select_sql_b, conn_yuqing_b)
    for i in  app_management_b.iterrows():
        update_sql_b = "UPDATE yuqing_b.weibo_content SET repost_content='" + urllib.unquote(urllib.unquote(i[1]["repost_content"])) + \
                     "' where docid='" + i[1]["docid"] + "'"
        cur_b.execute(update_sql_b)
        conn_yuqing_b.commit()
    # ls_id = app_management.get("account_id")
    # for i in ls_id:
    #     select_sql_weibo_account = "SELECT * FROM yuqing.weibo_management where account_id='" + i + "'"
    #     ls_weibo_account = pd.read_sql(select_sql_weibo_account, conn)
    #     weibo_account = ls_weibo_account.get("weibo_account")
    #     print i, weibo_account[0]
    #     update_sql = "UPDATE yuqing.weibo_content SET weibo_account='" + weibo_account[0] + \
    #                  "' where account_id='" + i + "'"
    #     update_sql_b = "UPDATE yuqing_b.weibo_content SET weibo_account='" + weibo_account[0] + \
    #                    "' where account_id='" + i + "'"



# 测试函数
if __name__ == "__main__":
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    conn_yuqing = connect_database(db_nick='yuqing')
    cur = conn_yuqing.cursor()
    climb_info(conn_yuqing, cur)
    climb_content(conn_yuqing, cur)
    # update_weibo_account(conn_yuqing, cur)
    # threads = []
    # threads.append(threading.Thread(target=climb_content, args=(conn_yuqing, cur)))
    # threads.append(threading.Thread(target=climb_info, args=(conn_yuqing, cur)))
    # for t in threads:
    #     t.setDaemon(True)
    #     t.start()
    # merge_update()
    cur.close()
    conn_yuqing.close()
    print "climb finish"




