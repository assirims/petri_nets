from models.place import Place
from models.transition import Transition
from models.connector import Connector
from lib.helper import Helper


class JsonToObjectParser(object):
    places = []
    connectors = []
    transitions = []

    def create_graph_structure(self, data):
        self._create_places(data["places"])
        self._create_connectors(data["connectors"])
        self._create_transitions(data["transitions"])

    def _create_places(self, places):
        for place in places:
            place_obj = Place(place["name"], place["id"], place["tokens"])
            self.places.append(place_obj)

    def _create_connectors(self, connectors):
        for connector in connectors:
            connector_obj = Connector(connector["id"], Helper.find_place_by_id(self.places, connector["place_id"]), connector["direction"], connector["weight"])
            self.connectors.append(connector_obj)

    def _create_transitions(self, transitions):
        for transition in transitions:
            connectors_in = []
            connectors_out = []
            for conn_id in transition["connectors_in_ids"]:
                connectors_in.append(Helper.find_connector_by_id(self.connectors, conn_id))
            for conn_id in transition["connectors_out_ids"]:
                connectors_out.append(Helper.find_connector_by_id(self.connectors, conn_id))

            transition_obj = Transition(connectors_in, connectors_out, transition["priority"], transition["id"], transition["name"])
            self.transitions.append(transition_obj)