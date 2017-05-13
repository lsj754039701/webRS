# -*- coding:utf-8 -*-
from baseHandler import baseHandler
import tornado.web
import model
import logging


class adminUpdateHandler(baseHandler):
    @tornado.web.authenticated
    def get(self):
        movie_id = self.get_argument('movie_id')
        movie_name = self.get_argument('movie_name')
        movie_type = self.get_argument('movie_type')
        movie_director = self.get_argument('movie_director')
        movie_stars = self.get_argument('movie_stars')
        movie_summary = self.get_argument('movie_summary')
        movie = model.mongo.find_movie_by_id(int(movie_id))[0]
        if movie_name:
            movie['name'] = movie_name
        if movie_type:
            movie['type'] = movie_type.split(';')
        if movie_director:
            movie['director'] = movie_director
        if movie_stars:
            movie['stars'] = movie_stars.split(';')
        if movie_summary:
            movie['summary'] = movie_summary
        print 'save: ', movie
        if model.mongo.save_movie(movie):
            self.redirect("/adminFind?movie_name=%s" % movie['name'])
            # self.render("/adminIndex")
