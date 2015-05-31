import ast

import tornado.ioloop
import tornado.web
import tornado.websocket

from utils.json_to_object_parser import JsonToObjectParser
from main import Main, RequestType


class Server(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message("Petri net simulation")

    def on_message(self, message):
        message_dict = ast.literal_eval(message)
        return self.__do_action(message_dict)

    def __do_action(self, message_dict):
        action_type = message_dict["type"]
        receive_data = message_dict["data"]

        if action_type is RequestType.START:
            parsed_objects = JsonToObjectParser()
            parsed_objects.create_graph_structure(receive_data)
            self.main = Main(parsed_objects.places, parsed_objects.transitions, parsed_objects.links)
            return self.write_message(self.main.start_simulation())
        elif action_type is RequestType.SIMULATE:
            return self.write_message(self.main.simulate())
        elif action_type is RequestType.GRAPH_FEATURES:
            return self.write_message(self.main.get_graph_features())

    def on_close(self):
        pass


class MainPage(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.render('/home/czis/Pulpit/index.html')


application = tornado.web.Application([
    (r"/", MainPage),
    (r"/websocket", Server),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()