# -*- coding=utf-8 -*-
import tornado.web
import tornado.ioloop
import os
import sys
import multiprocessing
import threading
import logging.config
from handler import *

logging.config.fileConfig('conf/log.conf')
handlers = [
    (r'/login', loginHandler),
    (r'/registe', registerHandler),
    (r'/index', indexHandler),
]

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'template/shop/one/home'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'debug': True,
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    'login_url': '/login'
}

def web_server(queue):
    print 'b'
    app = tornado.web.Application(handlers=handlers, **settings)
    app.listen(8000, address='localhost')
    tornado.ioloop.IOLoop.instance().start()

def rs_server(queue):
    print 'a'

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    webserver_pro = multiprocessing.Process(target=web_server, args=(queue,))
    rs_pro = multiprocessing.Process(target=rs_server, args=(queue,))
    webserver_pro.daemon = True
    rs_pro.daemon = True
    webserver_pro.start()
    rs_pro.start()
    webserver_pro.join()
    rs_pro.join()
    # from algorithm import *
    # c = cool()
    # c.calc()
    # user = {'age': 20, 'sex':'F', 'job': 'administrator'}
    # print c.recommend(user)

