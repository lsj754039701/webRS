# -*- coding:utf-8 -*-
import tornado.web
import model
from baseHandler import baseHandler


class registeHandler(baseHandler):
    def post(self, *args, **kwargs):
        user = {}
        user['nick'] = self.get_argument('nick')
        user['sex'] = self.get_argument('sex')
        user['age'] = self.get_argument('age')
        user['job'] = self.get_argument('job')
        user['account'] = self.get_argument('account')
        user['pwd'] = self.get_argument('pwd')
        users = model.get_all_user()
        flag = True
        for u in users:
            if u[5] == user['account']:
                flag = False
                break
        if flag:
            model.insert_user(user)
            self.set_secure_cookie('user', user['account'])
            self.render('index1.html')
        else:
            self.render('register.html', notify='')
