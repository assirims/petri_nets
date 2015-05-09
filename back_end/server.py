import tornado.ioloop
import tornado.web
import tornado.websocket


class Hello(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message("Hello, world")

    def on_message(self, message):
        self.write_message("Siemanko")

    def on_close(self):
        pass


class Main(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.render('/home/czis/Pulpit/index.html')


application = tornado.web.Application([
    (r"/", Main),
    (r"/websocket", Hello),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()