# -*- coding=utf-8 -*-
import tornado.web
from baseHandler import baseHandler
from algorithm import until
import model
import time
import logging


class buyMovieHandler(baseHandler):
    @tornado.web.authenticated
    def get(self):
        movie_id = self.get_argument("movie_id")
        user_id = self.get_secure_cookie("user")
        # print 'movieID, userID =>',  movie_id, user_id
        if ((user_id, movie_id) not in until.buyed) and (not model.is_buy(user_id, movie_id)):
            until.buyed.append((user_id, movie_id))
            logger = logging.getLogger('web')
            logger.info("get [buyMovie] user_id:%s movie_id:%s" % (user_id, movie_id))
            # model.insert_behaviors(((user_id, movie_id, 0, int(time.time())), ))
        self.redirect("/movieInfo?movie_id=%s" % str(movie_id))