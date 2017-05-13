# -*- coding:utf-8 -*-
import tornado.web
import model
import logging


class adminLoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('adminLogin.html', login='')
