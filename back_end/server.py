import ast
import tornado.ioloop
import tornado.web
import tornado.websocket
from lib.json_to_object_parser import JsonToObjectParser
from main import Main, RequestType


class Server(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message("Hello, world")

    def on_message(self, message):
        message_dict = ast.literal_eval(message)
        return self.__do_action(message_dict)

    def __do_action(self, message_dict):
        action_type = message_dict["type"]
        receive_data = message_dict["data"]

        if action_type is RequestType.START:
            parsed_objects = JsonToObjectParser()
            parsed_objects.create_graph_structure(receive_data)
            self.main = Main(parsed_objects.places, parsed_objects.transitions, parsed_objects.connectors)
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

# example data

{"type":1,
 "data": {
     "connectors": [
         {"id": 1, "place_id": 1, "direction": 1, "weight":1},
         {"id": 2, "place_id": 2, "direction": 2, "weight":1},
         {"id": 3, "place_id": 2, "direction": 1, "weight":1},
         {"id": 4, "place_id": 1, "direction": 2, "weight":1},
         {"id": 5, "place_id": 3, "direction": 2, "weight":2},
         {"id": 6, "place_id": 3, "direction": 1, "weight":1},
         {"id": 7, "place_id": 4, "direction": 2, "weight":3}
     ],
     "places": [
         {"id":1, "name":"p1", "tokens":1},
         {"id":2, "name":"p2", "tokens":0},
         {"id":3, "name":"p3", "tokens":1},
         {"id":4, "name":"p4", "tokens":0}
     ],
     "transitions": [
         {"connectors_in_ids": [1],
          "connectors_out_ids": [2],
          "priority": 5,
          "id": 1,
          "name": "t1"},
         {"connectors_in_ids": [3],
          "connectors_out_ids": [4,5],
          "priority": 1,
          "id": 2,
          "name": "t2"},
         {"connectors_in_ids": [6],
          "connectors_out_ids": [7],
          "priority": 2,
          "id": 3,
          "name": "t3"}
     ]
 }}