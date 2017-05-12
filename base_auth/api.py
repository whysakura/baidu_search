# -*- coding: utf-8 -*-
# @Time    : 2017/5/12 15:47
# @Author  : wrd
from tornado.web import  authenticated

from common.AuthClass import MyBaseHandler


class LoginHandler(MyBaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        self.set_secure_cookie("username", self.get_argument("username"))
        self.redirect(self.get_argument("next", "/"))


class LogoutHandler(MyBaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("username")
            self.redirect("/")