# -*- coding: utf-8 -*-
# Author:wrd
import logging
import logging.handlers
import pymysql
import time
import pytz
import datetime
import redis

from conf.setting import settings


class Logger(logging.Logger):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst = super(Logger,cls).__new__(cls,*args,**kwargs)
        return cls._inst

    def __init__(self, filename=None):
        super(Logger, self).__init__(self)
        # 日志文件名
        if filename is None:
            filename = 'test.log'
        self.filename = filename

        # 创建一个handler，用于写入日志文件 (每天生成1个，保留30天的日志)
        fh = logging.handlers.TimedRotatingFileHandler(self.filename, 'D', 1, 0)
        fh.suffix = "%Y%m%d-%H%M.log"
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s:%(filename)s[Line:%(lineno)d][thread:%(thread)s][process:%(process)s] %(levelname)s %(message)s',datefmt='%Y:%m:%d %H:%M:%S')
        fh.setFormatter(formatter)
        #ch.setFormatter(formatter)

        # 给logger添加handler
        self.addHandler(fh)
        self.addHandler(ch)

mylog = Logger(settings['log_path'])

class MyPyMysql(object):
    def __init__(self,**kwargs):
        try:
            self.connection = pymysql.connect(**kwargs)
        except Exception as e:
            mylog.error('数据库连接失败...')
            mylog.error(e)

    def query(self,sql,data=None):
        data = [] if data is None else data
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql,data)
                mylog.info(cursor._last_executed)
                self.connection.commit()
                result = cursor.fetchall()
                return result
        except Exception as e:
            self.connection.rollback()
            mylog.error('回滚: '+sql+str(data))
            mylog.error(e)

    @staticmethod
    def sql_splice(data):
        """
        sql 拼接
        :param data:
        :return:
        eg:
            sql_splice(data=[['1','2','3'],['a','b','c']])
            "('1', '2', '3'),('a', 'b', 'c')"
        """
        sql = []
        for i in data:
            tp = '("' + '","'.join(map(str, i)) + '")'
            sql.append(tp)

        return ','.join(sql)

    def insert_query(self,sql,data):
        data = MyPyMysql.sql_splice(data)
        self.query(sql %(data))

    def close_connect(self):
        self.connection.close()


def toMB(num):
    """
    b转换为Mb
    :param num:
    :return:
    """
    if num < 1024:
        return str(num) + 'B'
    elif num < 1024*1024:
        return str(round(num/1024.0,2)) + 'KB'
    else:
        return str(round(num/1048576.0, 2)) + 'M'


def _unicode(s):
    if isinstance(s, str):
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError:
            pass
    return s

class RedisPool(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls,'_inst'):
            cls._inst = super(RedisPool,cls).__new__(cls,*args,**kwargs)
        return cls._inst

    def __init__(self,**kwargs):
        self.pool = redis.ConnectionPool(**kwargs)

    def redis(self):
        rd = redis.Redis(connection_pool=self.pool)
        return rd

def timestamptotime(num):
    """
    时间戳转时间
    :param num:
    :return:
    """
    if num is None or not num:
        return ''
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.fromtimestamp(num, tz).strftime("%Y-%m-%d %H:%M:%S")

def getnowtime():
    """
    获取中国现在时间
    :return:
    """
    tz = pytz.timezone('Asia/Shanghai')
    return datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

if __name__ =='__main__':
    conf = {
        'host':'45.76.187.121',
        'port':6379,
        'password': 'w1314921',
        'db':0,
        'decode_responses':True
    }
    a = RedisPool(**conf).redis()
    dic = {"id": "1", "name": u"我是第一个用户"}
    iddic = {"id": "1", "name": u"我是第一个用户"}
    a.hmset("token001", dic)
    a.hmset("user_1", iddic)
    b=a.hgetall("token001")
    print(b)
    print(b['b'])
