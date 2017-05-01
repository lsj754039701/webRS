# -*- coding=utf-8 -*-
import tornado.web
from baseHandler import baseHandler
import model

class movieInfoHandler(baseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('movie.html')