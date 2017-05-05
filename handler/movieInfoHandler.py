# -*- coding=utf-8 -*-
import tornado.web
from baseHandler import baseHandler
import model
import logging
from algorithm import until


class movieInfoHandler(baseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        logger = logging.getLogger('web')
        user_id = self.get_secure_cookie("user")
        movie_id = self.get_argument("movie_id")
        logger.info('get [movieInfo] user_id:%s movie_id:%s' % (user_id, movie_id))
        movie = model.mongo.find_movie_by_id(int(movie_id))[0]
        movie['img_url'] = "images/movies/" + str(movie['_id']) + ".jpg"
        if (user_id, movie_id) in until.scored.keys():
            movie['score'] = until.scored[(user_id, movie_id)]
        elif (user_id, movie_id) in until.buyed:
            movie['score'] = (0, )
        else:
            movie['score'] = model.get_movie_score(user_id, movie_id)
        self.render('movie.html', movie=movie)