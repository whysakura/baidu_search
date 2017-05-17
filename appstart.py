# -*- coding: utf-8 -*-
# @Time    : 2017/5/15 10:43
# @Author  : wrd
import json

import tornado.escape
import tornado.gen
import tornado.httpclient
import tornado.ioloop
from tornado.httpserver import HTTPServer
from tornado.netutil import bind_sockets
from tornado.web import Application, url

from base_auth.api import LoginHandler, LogoutHandler
from common.AuthClass import PageNotFoundHandler
from conf.setting import settings
from main.api import Main, Timo

app = Application([
    url(r'/', Main, name='main_url'),
    url(r'/stroy/([0-9]+)',Timo,{'db':'haha'},name='story'),
    # url(r'/login', LoginHandler),
    # url(r'/logout', LogoutHandler),
    url('.*', PageNotFoundHandler)
], **settings)

if settings['ipv4']:
    import socket

    sockets = bind_sockets(8888, family=socket.AF_INET)
else:
    sockets = bind_sockets(8888)

# if not settings['debug']:
#     import tornado.process
#
#     tornado.process.fork_processes(0)  # 0 表示按 CPU 数目创建相应数目的子进程
server = HTTPServer(app, xheaders=True)
server.add_sockets(sockets)
tornado.ioloop.IOLoop.current().start()