# -*- coding: utf-8 -*-
# Author:wrd
import json

import tornado.escape
import tornado.gen
import tornado.httpclient
import tornado.ioloop
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado.web import Application, url

from conf.setting import settings, mysql_config
from common.utils import Logger, MyPyMysql, toMB
from common.AuthClass import MyBaseHandler, myauthenticated, PageNotFoundHandler

mylog = Logger(settings['log_path'])


class Main(MyBaseHandler):
    @myauthenticated
    def get(self):
        self.set_cookie('_xsrf_token', self.xsrf_token, httponly=True, secure=True)
        self.render('index.html', user=self.uname)

    def post(self):
        pmysql = MyPyMysql(**mysql_config)
        try:
            current_page = int(self.get_argument('currentPage'))
            searchvalue = '%' + self.get_argument('searchValue', '.').encode('utf-8') + '%' if self.get_argument(
                'searchValue', '') else ''
            limit = int(self.get_argument('pageSize'))
            response = {'error': '0'}
            start = limit * (current_page - 1)
            if not searchvalue:
                sql = """SELECT * FROM pt_db.spide_shares where share_time is not null  order by share_time desc limit %s,%s ;"""
                result = pmysql.query(sql, [start, limit])
                sql = """SELECT case when count(1) >100 then 100 else count(1) end as c FROM pt_db.spide_shares where share_time is not null;"""
                sumcount = pmysql.query(sql)
            else:
                sql = """SELECT * FROM pt_db.spide_shares where server_filename like %s order by share_time desc limit %s,%s;"""
                result = pmysql.query(sql, [searchvalue, start, limit])
                sql = """SELECT count(1) as c FROM pt_db.spide_shares where server_filename like %s ;"""
                sumcount = pmysql.query(sql, [searchvalue])
            if result and result is not None:
                tableData = [{
                                 'id': i['id'],
                                 'c_time': i['c_time'].strftime("%Y-%m-%d %H:%M:%S"),
                                 'uk': i['uk'],
                                 'username': i['username'],
                                 'server_filename_short': i['server_filename'][:12] + '...',
                                 'server_filename': i['server_filename'],
                                 'url': i['base_url'] + i['share_url'],
                                 'publics': '是' if i['public'] == '1' else '否',
                                 'size': toMB(i['size']),
                                 'uk_url': 'https://pan.baidu.com/share/home?uk=' + str(i['uk']),
                                 'share_time': i['share_time'].strftime("%Y-%m-%d %H:%M:%S") if i[
                                                                                                    'share_time'] is not None else ''
                             } for i in result]
            else:
                tableData = []
            response['tableData'] = tableData
            response['totals'] = sumcount[0]['c']
            self.write(json.dumps(response))
        except Exception as e:
            mylog.error(e)
            response = {'error': '-1'}
            self.write(json.dumps(response))
        finally:
            pmysql.close_connect()
        self.finish()


class Timo(MyBaseHandler):
    def initialize(self, db):
        self.db = db

    def get(self, story_id):
        self.write('this story_id is :%s,db is %s' % (story_id, self.db))


class MainHandler(MyBaseHandler):
    @tornado.gen.coroutine
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        response = yield http.fetch("http://www.dongwm.com/tags/")
        self.write("Fetched " + str(response.body) + " entries "
                                                     "from the FriendFeed API")


app = Application([
    url(r'/', Main, name='main_url'),
    # url(r'/stroy/([0-9]+)',Timo,{'db':'haha'},name='story'),
    # url(r'/login', LoginHandler),
    # url(r'/logout', LogoutHandler),
    url('.*', PageNotFoundHandler)
], **settings)

if settings['ipv4']:
    import socket

    sockets = bind_sockets(8888, family=socket.AF_INET)
else:
    sockets = bind_sockets(8888)

if not settings['debug']:
    import tornado.process

    tornado.process.fork_processes(0)  # 0 表示按 CPU 数目创建相应数目的子进程
server = HTTPServer(app, xheaders=True)
server.add_sockets(sockets)
tornado.ioloop.IOLoop.current().start()
