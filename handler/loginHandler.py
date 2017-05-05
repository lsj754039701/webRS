# -*- coding:utf-8 -*-
import tornado.web
import model
import logging


class loginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')

    def post(self, *args, **kwargs):
        logger = logging.getLogger('web')
        req_type = self.get_argument('reqType')
        if req_type == 'alterPwd':
            act = self.get_argument('account')
            oldpwd = self.get_argument('oldpwd')
            if model.login(act, oldpwd):
                logger.info('post [alterPwd] user_act:%s' % act  )
                newpwd = self.get_argument('newpwd')
                model.alter_pwd(act, newpwd)
                self.get()
            else:
                self.render('alterPwd.html')
