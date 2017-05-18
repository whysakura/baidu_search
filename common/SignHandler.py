# -*- coding: utf-8 -*-
# @Time    : 2017/5/18 14:33
# @Author  : wrd
import time
import tornado.ioloop

from common.utils import Logger
from conf.setting import settings, MAX_WAIT_SECONDS_BEFORE_SHUTDOWN

mylog = Logger(settings['log_path'])

def sig_handler(server, sig, frame):
    io_loop = tornado.ioloop.IOLoop.instance()

    def stop_loop(deadline):
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            mylog.info('Waiting for next tick')
            io_loop.add_timeout(now + 1, stop_loop, deadline)
        else:
            io_loop.stop()
            mylog.info('Shutdown finally')

    def shutdown():
        mylog.info('Stopping http server')
        server.stop()
        mylog.info('Will shutdown in %s seconds ...',MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)
        stop_loop(time.time() + MAX_WAIT_SECONDS_BEFORE_SHUTDOWN)

        mylog.warning('Caught signal: %s', sig)
    io_loop.add_callback_from_signal(shutdown)