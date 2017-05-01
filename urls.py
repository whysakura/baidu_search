# -*- coding: utf-8 -*-
# Author:wrd
import os

import tornado.gen
import tornado.httpclient
import tornado.escape
import tornado.ioloop
from tornado.web import RequestHandler, Application, url


class Main(RequestHandler):
    def get(self):
        items = {
            "roads":'weiruduan',
            "wood":'weiruduan1',
            "made":'shaooooo',
            "difference":'yooooooooooooooo',
        }
        self.render('index.html',**items)


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
    "xsrf_cookies": True,
    "template_path":os.path.join(os.path.dirname(__file__), "templates"),
    'debug' : True
}

app = Application([
    url(r'/',Main),
    url(r'/stroy/([0-9]+)',Timo,{'db':'haha'},name='story'),
], **settings)


app.listen(8888)
tornado.ioloop.IOLoop.current().start()