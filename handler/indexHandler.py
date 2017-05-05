# -*- coding=utf-8 -*-
import tornado.web
from baseHandler import baseHandler
import model
from algorithm import manager
import logging
from algorithm import until

class indexHandler(baseHandler):
    def recommend(self, user):
        until.lock.acquire()
        rec_movies = manager.rs_manager.recommend(user)
        until.lock.release()

        new_movies = []
        for title, movies in rec_movies:
            tmp_movies = []
            for movie_id, rate in movies:
                movie = model.mongo.find_movie_by_id(movie_id)[0]
                movie['img_url'] = "images/movies/" + str(movie['_id']) + ".jpg"
                movie['cnt'] = model.get_movie_cnt(movie_id)
                # movie['img_url'] = "images/movies/" + "1" + ".jpg"
                tmp_movies.append(movie)
            new_movies.append((title, tmp_movies))
        return new_movies


    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        act = self.get_argument('id')
        pwd = self.get_argument('pwd')
        if model.login(act, pwd):
            logger = logging.getLogger('web')
            logger.info('post [login] user_act:%s' % act)
            user = model.find_user_by_account(act)
            new_movies = self.recommend(user)
            self.set_secure_cookie('user', str(user[0]))
            self.render('index1.html', rec_movies=new_movies)
        else:
            self.render('login.html')

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user = model.get_user_by_id(self.get_secure_cookie('user'))
        new_movies = self.recommend(user)
        self.render('index1.html', rec_movies=new_movies)