# -*- coding: utf-8 -*-
# Author:wrd
import os
import random

import pymysql

settings = {
    "static_path": os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"),
    "cookie_secret": "TqSJJ95uQ+Klsn0pmJF3IGwTaU35wEvNucDwCqfYGpU=",
    "login_url": "/login",
    "xsrf_cookies": True,
    "template_path":os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
    'debug' : True,
    'log_path':os.path.join(os.path.dirname(os.path.dirname(__file__)), "logger",'error.log'),
    'ipv4':True,
    'gzip': True,

}
mysql_config = {
    'host': '120.26.214.19',
    'port': 3306,
    'user': 'root',
    'password': 'putao1234',
    'db': 'pt_db',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

redis_conf = {
    'host': '45.76.187.121',
    'port': 6379,
    'password': 'w1314921',
    'db':0,
    'decode_responses':True
}
# 等待结束时间
MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 5
# 监听端口
LISTEN_PORT = 8888