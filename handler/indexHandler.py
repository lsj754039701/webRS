# -*- coding=utf-8 -*-
import tornado.web
from baseHandler import baseHandler
import model


class indexHandler(baseHandler):
    def post(self, *args, **kwargs):
        id = self.get_argument('id')
        pwd = self.get_argument('pwd')
        if model.login(id, pwd):
            self.set_secure_cookie('user', id)
            self.render('index1.html')
        else:
            self.render('login.html')

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('index1.html')