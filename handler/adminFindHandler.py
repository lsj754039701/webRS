# -*- coding:utf-8 -*-
from baseHandler import baseHandler
import tornado.web
import model
import logging


class adminFindHandler(baseHandler):
    @tornado.web.authenticated
    def get(self):
        print 'find:'
        movie_name = self.get_argument("movie_name")
        movie = model.mongo.find_movie_by_name(movie_name)
        self.render("updateMovie.html", movie=movie[0])
