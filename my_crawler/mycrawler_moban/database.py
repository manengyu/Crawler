# -*- coding: utf8 -*-
import time
import logging
from sql import *
import pandas as pd
import MySQLdb
from pyhive import presto


def initlogging(logfilename):
    logging.basicConfig(
        level=logging.DEBUG,
        format=u"%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s",
        datefmt=u"%m-%d %H:%M",
        filename=logfilename,
        filemode=u"w")
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    # set a format which is simpler for console use
    formatter = logging.Formatter(u"%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s")
    # tell the handler to use this format
    console.setFormatter(formatter)
    logging.getLogger(u"").addHandler(console)
    return logging


def connect_database(db_nick=u""):  # 连接数据库
    conn = u""
    if db_nick == u"Data":
        while True:
            try:
                conn = MySQLdb.connect(host=u"", user=u"", passwd=u"",
                                       db=u"", port=3306, charset=u"utf8")
                break
            except MySQLdb.Error, e:
                logging.error(u"Mysql Error %d: %s", e.args[0], e.args[1])
    elif db_nick == u"presto":
        while True:
            try:
                conn = presto.connect(host=u'', port=9090, catalog=u"", username=u"", schema=u"")
                break
            except presto.ProgrammingError as e:
                logging.error(u"Presto Error %d: %s", e.args[0], e.args[1])
    else:
        print u"No such database!!!"
    return conn

mylogging = initlogging(u"./get_.log")
conn_mysql = connect_database(u"Data")  # 创建MySQL,Presto连接
cur_mysql = conn_mysql.cursor()
conn_presto_0820 = connect_database(u"presto")
cur_presto = conn_presto_0820.cursor()


def sql_select_mysql(sql, *args):
    cur_mysql.execute(sql % args)
    return cur_mysql.fetchall()


def sql_select_pd(sql, type_conn=u"presto"):
    return pd.read_sql(sql, conn_mysql if type_conn == u"mysql" else conn_presto_0820)


def sql_upt_mysql(sql, *args):
    print(u"upt", sql, args)
    # cur_mysql.execute(sql % args)
    # conn_mysql.commit()
    # return cur_mysql.fetchall()
    

def error_to_db(error_info):
    try:
        sql_upt_mysql(u"", error_info)
    except Exception as e:
        logging.error(e)
