# -*- coding=utf-8 -*-
import tornado.web
from baseHandler import baseHandler
import model
import logging

class adminIndexHandler(baseHandler):
    def post(self, *args, **kwargs):
        act = self.get_argument('id')
        pwd = self.get_argument('pwd')
        print act, pwd
        if model.admin_login(act, pwd):
            logger = logging.getLogger('web')
            logger.info('post [adminLogin] ')
            self.set_secure_cookie('user', "admin")
            self.render("adminIndex.html")
        else:
            self.render('adminLogin.html', login='账号密码错误')

    # @tornado.web.authenticated
    # def get(self, *args, **kwargs):
    #     user = model.get_user_by_id(self.get_secure_cookie('user'))
    #     new_movies = self.recommend(user)
    #     self.render('index1.html', rec_movies=new_movies)

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        print 'index get    '
        self.render("adminIndex.html")