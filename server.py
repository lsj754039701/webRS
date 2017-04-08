import tornado.web
import tornado.ioloop
import os
import sys
import multiprocessing
from handler import *

from tornado.web import StaticFileHandler

handlers = [
    (r'/login', loginHandler),
    (r'/registe', registerHandler),
    (r'/index', indexHandler)
]

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'template/shop/one/home'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'debug': True
}

if __name__ == '__main__':
    app = tornado.web.Application(handlers=handlers, **settings)
    app.listen(8000, address='localhost')
    tornado.ioloop.IOLoop.instance().start()
