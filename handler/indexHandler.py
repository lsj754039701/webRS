import tornado.web


class indexHandler(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        id = self.get_argument('id')
        pwd = self.get_argument('pwd')
        if id == 'zll' and pwd == 'zll':
            self.render('index1.html')