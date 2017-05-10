# -*- coding: utf-8 -*-
# Author:wrd
import os
import random

import pymysql

settings = {
    "static_path": os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"),
    # "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": False,
    "template_path":os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
    'debug' : True,
    'log_path':os.path.join(os.path.dirname(os.path.dirname(__file__)), "logger",'error.log')

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