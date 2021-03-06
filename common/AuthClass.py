# -*- coding: utf-8 -*-
# @Time    : 2017/5/12 16:14
# @Author  : wrd
import functools
from tornado.web import RequestHandler, HTTPError
from common.utils import MyPyMysql, getnowtime
from conf.setting import mysql_config


class MyBaseHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        self.render('500.html',user=self.get_current_user(),status_code=status_code)

    def get_current_user(self):
        return self.get_secure_cookie("username")


class PageNotFoundHandler(MyBaseHandler):
    def get(self):
        raise HTTPError(404)


def add_tourist(remote_ip):
    """
    添加游客身份
    :return:
    """
    pmysql = MyPyMysql(**mysql_config)
    sql = """insert into pt_db.spide_user_id (ip) values (%s) ON DUPLICATE KEY UPDATE  m_time = %s;"""
    pmysql.query(sql, (remote_ip, getnowtime()))
    sql = """select id from pt_db.spide_user_id where ip = %s;"""
    result = pmysql.query(sql, (remote_ip))
    return '游客 ' + str(result[0]['id'])


def myauthenticated(method):
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            remote_ip = self.request.remote_ip
            uname = add_tourist(remote_ip)
            self.set_secure_cookie("username", uname)
            self.uname = uname
            # if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # jQuery 等库会附带这个头
            #     self.set_header('Content-Type', 'application/json; charset=UTF-8')
            #     self.write(json.dumps({'success': False, 'msg': u'您的会话已过期，请重新登录！'}))
            # if self.request.method in ("GET", "HEAD"):
            #     url = self.get_login_url()
            #     if "?" not in url:
            #         if urlparse.urlsplit(url).scheme:
            #             # if login url is absolute, make next absolute too
            #             next_url = self.request.full_url()
            #         else:
            #             next_url = self.request.uri
            #         url += "?" + urlencode(dict(next=next_url))
            #     self.redirect(url)
            #     return
            # raise HTTPError(403)
        else:
            self.uname = self.get_current_user()
        return method(self, *args, **kwargs)

    return wrapper
