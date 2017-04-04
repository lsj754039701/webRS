import tornado.web

class registerHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('register.html')