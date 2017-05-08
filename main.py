# -*- coding: utf-8 -*-
# Author:wrd
import json
import os
import random

import pymysql
import tornado.gen
import tornado.httpclient
import tornado.escape
import tornado.ioloop
from tornado.web import RequestHandler, Application, url

from utils import MyPyMysql


class Main(RequestHandler):
    def get(self):
        self.render('index.html')
    def post(self):
        try:
            current_page = int(self.get_argument('currentPage'))
            searchvalue = '%'+self.get_argument('searchValue','.').encode('utf-8')+'%' if  self.get_argument('searchValue','.') else '%.%'
            limit = int(self.get_argument('pageSize'))
            response = {'error':'0'}
            pmysql = MyPyMysql(**mysql_config)
            sql = """SELECT * FROM pt_db.spide_shares where server_filename like %s order by id desc limit 300 ;"""
            result = pmysql.query(sql,[searchvalue])
            if result and result is not None:
                tableData = [{
                                'id':i['id'],
                                'c_time':i['c_time'].strftime("%Y-%m-%d %H:%M:%S"),
                                'uk':i['uk'],
                                'username':i['username'],
                                'server_filename_short':i['server_filename'][:12]+'...',
                                'server_filename':i['server_filename'],
                                'url':i['base_url']+i['share_url'],
                                'publics':'是' if i['public']=='1' else '否',
                                'size':str(round(i['size']/1048576.0,2)) + 'M'
                              } for i in result]
            else:
                tableData = []
            start = limit*(current_page-1)
            end = limit*(current_page)
            response['tableData'] = tableData[start:end]
            response['totals'] = len(tableData)
            self.write(json.dumps(response))
        except:
            response = {'error':'-1'}
            self.write(json.dumps(response))
        self.finish()

class Timo(RequestHandler):
    def initialize(self,db):
        self.db = db
    def get(self,story_id):
        self.write('this story_id is :%s,db is %s' %(story_id,self.db))

class MainHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://www.dongwm.com/tags/")
        self.write("Fetched " + str(response.body) + " entries "
                   "from the FriendFeed API")

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    # "cookie_secret": "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    "login_url": "/login",
    "xsrf_cookies": False,
    "template_path":os.path.join(os.path.dirname(__file__), "templates"),
    'debug' : True

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

app = Application([
    url(r'/',Main,name='main_url'),
    url(r'/stroy/([0-9]+)',Timo,{'db':'haha'},name='story'),
], **settings)


app.listen(8888)
tornado.ioloop.IOLoop.current().start()