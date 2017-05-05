# -*- coding=utf-8 -*-
import tornado.web
from baseHandler import baseHandler
from algorithm import until
import logging


class scoreMvoieHandler(baseHandler):
    @tornado.web.authenticated
    def get(self):
        movie_id = self.get_argument("movie_id")
        user_id = self.get_secure_cookie("user")
        score = self.get_argument("score")
        until.scored[(user_id, movie_id)] = score
        # print 'score: movieID, userID, score =>',  movie_id, user_id, score
        # if model.update_user_behavior(user_id, movie_id, score):
        logger = logging.getLogger('web')
        logger.info("get [scoreMovie] user_id:%s movie_id:%s score:%s" % (user_id, movie_id, score))
        # else:
        #     print 'score error'
        self.redirect("/movieInfo?movie_id=%s" % str(movie_id))