import random
from utils.coverability_graph import CoverabilityGraph
from utils.helper import Helper
from utils.incidence_matrix_creator import IncidenceMatrixCreator


class RequestType(object):
    START = 1
    SIMULATE = 2
    GRAPH_FEATURES = 3
    END = 4


class GraphFeatureType(object):
    INCIDENCE_MATRIX = 1
    LIVE_TRANSITIONS = 2
    COVERABILITY_GRAPH = 3


class Main(object):

    def __init__(self, places, transitions, connectors):
        self.places = places
        self.transitions = transitions
        self.connectors = connectors

    def __json_type_wrapper(self, type, data=None):
        return '{"type": %s, "data": %s}' % (type, data)

    def start_simulation(self):
        return '{"type": %s, "data": ""}' % RequestType.START

    def simulate(self):
        transition = random.sample(self.transitions, 1)[0]
        if transition.is_doable():
            priority_queue = Helper.get_competitive_transitions_priority_queue(self.transitions, transition)
            if transition is priority_queue.get():
                transition.run_transition()
                return self.__json_type_wrapper(RequestType.SIMULATE, transition.to_json())
            else:
                return self.__json_type_wrapper(RequestType.SIMULATE, transition.to_json())
        else:
            return self.__json_type_wrapper(RequestType.SIMULATE, transition.to_json())

    def get_graph_features(self):
        data = {
            GraphFeatureType.INCIDENCE_MATRIX: self.__get_incidence_matrix().tolist(),
            GraphFeatureType.LIVE_TRANSITIONS: self.__get_live_transitions_ids(),
            GraphFeatureType.COVERABILITY_GRAPH: self.__get_coverability_graph()
        }

        return self.__json_type_wrapper(RequestType.GRAPH_FEATURES, data)

    def __get_incidence_matrix(self):
        incidence_matrix_creator = IncidenceMatrixCreator(self.places, self.transitions, self.connectors)
        return incidence_matrix_creator.create_incidence_matrix()

    def __get_live_transitions_ids(self):
        live_transitions_ids = []
        for transition in self.transitions:
            if transition.is_doable():
                live_transitions_ids.append(transition.id)
        return live_transitions_ids

    def __get_coverability_graph(self):
        coverability_graph = CoverabilityGraph(self.transitions)
        return coverability_graph.get_coverability_graph()