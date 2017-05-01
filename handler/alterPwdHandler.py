# -*- coding=utf-8 -*-
import tornado.web

class alterPwdPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('alterPwd.html')


class alterPwdHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        self.render('alterPwd.html')