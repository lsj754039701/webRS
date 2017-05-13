# -*- coding:utf-8 -*-
import tornado.web
import logging


class signoutHandler(tornado.web.RequestHandler):
    def get(self):
        print 'logout'
        self.clear_cookie("user")
        self.redirect("/login")