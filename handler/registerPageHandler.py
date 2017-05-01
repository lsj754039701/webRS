import tornado.web


class registerPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html', notify='hidden')