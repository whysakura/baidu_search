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