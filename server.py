# -*- coding=utf-8 -*-
import tornado.web
import tornado.ioloop
import os
import logging.config
from algorithm import manager
import threading
from handler import *
import time
from algorithm import until


logging.config.fileConfig('conf/log.conf')
handlers = [
    (r'/login', loginHandler),
    (r'/registePage', registerPageHandler),
    (r'/index', indexHandler),
    (r'/alterPwdPage', alterPwdPageHandler),
    (r'/alterPwd', alterPwdHandler),
    (r'/movieInfo', movieInfoHandler),
    (r'/registe', registeHandler),
    (r'/buyMovie', buyMovieHandler),
    (r'/scoreMovie', scoreMvoieHandler),
]

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'template/shop/one/home'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'debug': True,
    "cookie_secret": "bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
    'login_url': '/login'
}

def web_server():
    print 'web_server start'
    app = tornado.web.Application(handlers=handlers, **settings)
    app.listen(8000, address='localhost')
    tornado.ioloop.IOLoop.instance().start()


def rs_server():
    print 'rs_server start'
    logger = logging.getLogger()
    while True:
        time.sleep(100)
        print 'start update rs_manager'
        until.scored = {}
        until.buyed = []
        until.webLog.web_mongo()
        until.webLog.add_behavior()
        until.lock.acquire()
        new_manager = manager.rsManager()
        logger.info("start update rs_manager")
        manager.rs_manager.update(new_manager)
        logger.info("end update rs_manager")
        print 'end update rs_manager'
        until.lock.release()


if __name__ == '__main__':
    rs_update = threading.Thread(target=rs_server)
    rs_update.setDaemon(True)
    rs_update.start()
    # until.webLog.update_manager()
    web_server()

    # from spider import spider_movies
    # spider_movies.spider_imgs()


    # from algorithm import *
    #
    # itemCF = CF.itemCF
    # itemCF.cacl_simi()
    # rank = itemCF.recommend(447)
    # print rank[:10]
    # print itemCF.precision()
    # print itemCF.recall()
    # print itemCF.coverage()



    # from algorithm import *
    # c = manager.rsManager()
    # user = {'id': 61, 'age': 20, 'sex': 'F', 'job': 'administrator'}
    # movie = {
    #     'type': ['Mystery', 'Sci-Fi', 'Crime', 'Romance',  'Animation', 'Action', 'Comedy', 'Documentary',
    #              'Musical', 'Drama', 'Horror']}
    # print c.recommend(user)

    # import model
    # from algorithm import cool
    # c = cool.cool()
    # user = {'age': 20, 'sex':'F', 'job': 'administrator'}
    # movies = c.recommend(user)
    # for movie_id, rate in movies[:3]:
    #     print model.mongo.find_movie_by_id(movie_id)




