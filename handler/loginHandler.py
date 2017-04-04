import tornado.web

class loginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')