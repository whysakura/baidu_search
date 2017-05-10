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

from conf.setting import settings, mysql_config
from utils import  Logger,MyPyMysql, toMB

mylog = Logger(settings['log_path'])

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
            sql = """SELECT * FROM pt_db.spide_shares where share_time is not null and server_filename like %s order by share_time desc limit 100 ;"""
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
                                'size':toMB(i['size']),
                                'uk_url':'https://pan.baidu.com/share/home?uk='+str(i['uk']),
                                'share_time':i['share_time'].strftime("%Y-%m-%d %H:%M:%S") if i['share_time'] is not None else ''
                              } for i in result]
            else:
                tableData = []
            start = limit*(current_page-1)
            end = limit*(current_page)
            response['tableData'] = tableData[start:end]
            response['totals'] = len(tableData)
            self.write(json.dumps(response))
        except Exception as e:
            mylog.error(e)
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



app = Application([
    url(r'/',Main,name='main_url'),
    url(r'/stroy/([0-9]+)',Timo,{'db':'haha'},name='story'),
], **settings)


app.listen(8888)
tornado.ioloop.IOLoop.current().start()