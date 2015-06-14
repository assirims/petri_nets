import os
import ast
import json
import tornado.ioloop
import tornado.web
import tornado.websocket

from utils.json_to_object_parser import JsonToObjectParser
from main import Main, RequestType


class Server(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message(json.dumps({"message": "Petri net simulation"}))

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
            try:
                return self.write_message(self.main.simulate())
            except AttributeError:
                return self.write_message(json.dumps({'error': 'Network is empty. Please send network parameters first.'}))
        elif action_type is RequestType.GRAPH_FEATURES:
            try:
                return self.write_message(self.main.get_graph_features())
            except AttributeError:
                return self.write_message(json.dumps({'error': 'Network is empty. Please send network parameters first.'}))
        elif action_type is RequestType.VECTOR_NETWORK_CONSERVATIVE:
            try:
                return self.write_message(self.main.is_network_vector_conservative(ast.literal_eval(receive_data)))
            except AttributeError:
                return self.write_message(json.dumps({'error': 'Network is empty. Please send network parameters first.'}))
        elif action_type is RequestType.LIVE_TRANSITIONS:
            try:
                return self.write_message(self.main.get_live_transitions())
            except AttributeError:
                return self.write_message(json.dumps({'error': 'Network is empty. Please send network parameters first.'}))
        elif action_type is RequestType.RUN_SELECTED_TRANSITION:
            try:
                return self.write_message(self.main.run_selected_transitions(receive_data))
            except AttributeError:
                return self.write_message(json.dumps({'error': 'Network is empty. Please send network parameters first.'}))

    def on_close(self):
        pass


class MainPage(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        # self.render(root) # local dev mode
        self.render(os.path.join(root, '../front_end/index.html'))

# root = '/home/czis/Pulpit/index.html' # local dev mode
root = os.path.dirname(__file__)

application = tornado.web.Application([
    (r"/", MainPage),
    (r"/websocket", Server),
], debug=True, static_path=os.path.join(root, '../front_end'))

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()