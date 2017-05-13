# -*- coding:utf-8 -*-
import tornado.web
from baseHandler import baseHandler
import model
import logging
from spider import spider_movies


class adminAddHandler(baseHandler):
    @tornado.web.authenticated
    def get(self):
        movies = self.get_argument("movies")
        movies = movies.split("\n")
        movies = [movie.strip() for movie in movies]
        success = spider_movies.spider_movies(movies)
        res = [movie['name'] for movie in success]
        self.render("addMovie.html", success='; '.join(res))
