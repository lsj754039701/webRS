# -*- coding:utf-8 -*-
import tornado.web
import model
import logging


class adminEventHandler(tornado.web.RequestHandler):
    def get(self):
        event = self.get_argument("event")
        if event == "add":
            self.render("addMovie.html", success=None)
        elif event == "find":
            self.render("findMovie.html")


