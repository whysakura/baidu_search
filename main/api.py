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

from base_auth.api import LoginHandler, LogoutHandler
from conf.setting import settings, mysql_config, redis_conf
from common.utils import Logger, MyPyMysql, toMB, timestamptotime
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
            searchvalue = self.get_argument('searchValue', '.').encode('utf-8') if self.get_argument(
                'searchValue', '') else ''
            limit = int(self.get_argument('pageSize'))
            response = {'error': '0'}
            start = limit * (current_page - 1)
            if not searchvalue:
                sql = """SELECT id,server_filename,username,UNIX_TIMESTAMP(share_time) as share_time,
                          UNIX_TIMESTAMP(c_time) as c_time,base_url,uk,share_url,
                          `public`,`size`
                          FROM pt_db.spide_shares where share_time is not null  order by share_time desc limit %s,%s ;"""
                result = pmysql.query(sql, [start, limit])
                sql = """SELECT case when count(1) >100 then 100 else count(1) end as c FROM pt_db.spide_shares where share_time is not null;"""
                sumcount = pmysql.query(sql)
                if result and result is not None:
                    tableData = [{
                                     'id': i['id'],
                                     'c_time': timestamptotime(i['c_time']),
                                     'uk': i['uk'],
                                     'username': i['username'],
                                     'server_filename_short': i['server_filename'][:12] + '...',
                                     'server_filename': i['server_filename'],
                                     'url': i['base_url'] + i['share_url'],
                                     'publics': '是' if i['public'] == '1' else '否',
                                     'size': toMB(i['size']),
                                     'uk_url': 'https://pan.baidu.com/share/home?uk=' + str(i['uk']),
                                     'share_time': timestamptotime(i['share_time'])
                                 } for i in result]
                else:
                    tableData = []

                response['totals'] = sumcount[0]['c']
            else:
                from sphinxapi import *
                cl = SphinxClient()
                cl.SetServer(redis_conf['host'], 9312)  # 主机与端口
                cl.SetSortMode(SPH_SORT_EXTENDED, "share_time DESC")
                cl.SetMatchMode(SPH_MATCH_EXTENDED2)
                cl.SetLimits(start, limit)
                searchvalue = searchvalue.replace(' ','').replace(' ','&')
                res = cl.Query(searchvalue, 'app')
                mylog.info('查找- ' + searchvalue)
                if res['error']:
                    mylog.error(res['error'])
                sumcount = res['total']
                tableData = [{
                                 'id': i['id'],
                                 'c_time': timestamptotime(i['attrs']['c_time']),
                                 'uk': i['attrs']['uk'],
                                 'username':  i['attrs']['username'].decode('utf-8'),
                                 'server_filename_short': i['attrs']['server_filename'].decode('utf-8')[:12] + '...',
                                 'server_filename': i['attrs']['server_filename'].decode('utf-8'),
                                 'url': i['attrs']['base_url'] + i['attrs']['share_url'],
                                 'publics': '是' if i['attrs']['public'] == '1' else '否',
                                 'size': toMB(i['attrs']['size']),
                                 'uk_url': 'https://pan.baidu.com/share/home?uk=' + str(i['attrs']['uk']),
                                 'share_time': timestamptotime(i['attrs']['share_time'])
                             } for i in res['matches']]
                # sql = """SELECT id,server_filename,username,UNIX_TIMESTAMP(share_time) as share_time,
                #           UNIX_TIMESTAMP(c_time) as c_time,base_url,uk,share_url,
                #           `public`,`size` FROM pt_db.spide_shares where server_filename like %s order by share_time desc limit %s,%s;"""
                # result = pmysql.query(sql, [searchvalue, start, limit])
                # sql = """SELECT count(1) as c FROM pt_db.spide_shares where server_filename like %s ;"""
                # sumcount = pmysql.query(sql, [searchvalue])

                response['totals'] = sumcount
            response['tableData'] = tableData
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


