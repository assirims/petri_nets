from models.place import Place
from models.transition import Transition
from models.link import Connector
from lib.helper import Helper


class JsonToObjectParser(object):
    def __init__(self):
        self.places = []
        self.links = []
        self.transitions = []

    def create_graph_structure(self, data):
        self._create_places(data["places"])
        self._create_links(data["links"])
        self._create_transitions(data["transitions"])

    def _create_places(self, places):
        for place in places:
            place_obj = Place(place["name"], place["id"], place["tokens"])
            self.places.append(place_obj)

    def _create_links(self, links):
        for link in links:
            link_obj = Connector(link["id"], Helper.find_place_by_id(self.places, link["place_id"]), link["direction"], link["weight"])
            self.links.append(link_obj)

    def _create_transitions(self, transitions):
        for transition in transitions:
            links_in = []
            links_out = []
            for conn_id in transition["links_in_ids"]:
                links_in.append(Helper.find_link_by_id(self.links, conn_id))
            for conn_id in transition["links_out_ids"]:
                links_out.append(Helper.find_link_by_id(self.links, conn_id))

            transition_obj = Transition(links_in, links_out, transition["priority"], transition["id"], transition["name"])
            self.transitions.append(transition_obj)