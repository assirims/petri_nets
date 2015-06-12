import random
import json
from lib.bounded_checker import BoundedChecker
from lib.conservative_checker import ConservativeChecker
from lib.coverability_graph import CoverabilityGraph
from lib.liveness_checker import LivenessChecker

from lib.reachability_graph import ReachabilityGraph
from lib.helper import Helper
from lib.incidence_matrix_creator import IncidenceMatrixCreator
from lib.reversibility_checker import ReversibilityChecker


class RequestType(object):
    START = 1
    SIMULATE = 2
    GRAPH_FEATURES = 3
    VECTOR_NETWORK_CONSERVATIVE = 4
    END = 5


class GraphFeatureType(object):
    INCIDENCE_MATRIX = 1
    LIVE_TRANSITIONS = 2
    REACHABILITY_GRAPH = 3
    COVERABILITY_GRAPH = 4
    PLACES_K_BOUNDED = 5
    IS_NETWORK_K_BOUNDED = 6
    IS_NETWORK_SAFE = 7
    IS_NETWORK_CONSERVATIVE = 8
    IS_NETWORK_LIVE = 9
    TRANSITIONS_LIVENESS = 10
    IS_NETWORK_REVERSIBLE = 11


class Main(object):

    def __init__(self, places, transitions, links):
        self.places = places
        self.transitions = transitions
        self.links = links

    def __json_type_wrapper(self, type, data=None, partially_converted_to_json=False):
        if partially_converted_to_json:
            return json.dumps({"type": type, "data": json.loads(data)})

        return json.dumps({"type": type, "data": data})

    def start_simulation(self):
        return self.__json_type_wrapper(RequestType.START)

    def simulate(self):
        live_transitions = self.__get_live_transitions()

        if not live_transitions:
            return self.__json_type_wrapper(RequestType.END)

        transition = random.sample(live_transitions, 1)[0]

        priority_queue = Helper.get_competitive_transitions_priority_queue(self.transitions, transition)
        transition = priority_queue.get()
        transition.run_transition()

        return self.__json_type_wrapper(RequestType.SIMULATE, transition.to_json(), True)

    def get_graph_features(self):
        data = {
            GraphFeatureType.INCIDENCE_MATRIX: self.__get_incidence_matrix().tolist(),
            GraphFeatureType.LIVE_TRANSITIONS: self.__get_live_transitions_ids(),
            GraphFeatureType.REACHABILITY_GRAPH: self.__get_reachability_graph(),
            GraphFeatureType.COVERABILITY_GRAPH: self.__get_coverability_graph(),
            GraphFeatureType.PLACES_K_BOUNDED: self.__get_places_k_bounded(),
            GraphFeatureType.IS_NETWORK_K_BOUNDED: self.__is_network_k_bounded(),
            GraphFeatureType.IS_NETWORK_SAFE: self.__is_network_safe(),
            GraphFeatureType.IS_NETWORK_CONSERVATIVE: self.__is_network_conservative(),
            GraphFeatureType.IS_NETWORK_LIVE: self.__is_network_live(),
            GraphFeatureType.TRANSITIONS_LIVENESS: self.__transitions_liveness(),
            GraphFeatureType.IS_NETWORK_REVERSIBLE: self.__is_network_reversible()
        }

        return self.__json_type_wrapper(RequestType.GRAPH_FEATURES, data)

    def is_network_vector_conservative(self, vector_coefficients):
        states_list = CoverabilityGraph(self.transitions).get_graph()
        conservative_checker = ConservativeChecker(self.places, states_list)
        return self.__json_type_wrapper(RequestType.VECTOR_NETWORK_CONSERVATIVE, conservative_checker.is_network_conservative(vector_coefficients))

    def __get_incidence_matrix(self):
        incidence_matrix_creator = IncidenceMatrixCreator(self.places, self.transitions, self.links)
        return incidence_matrix_creator.create_incidence_matrix()

    def __get_live_transitions_ids(self):
        live_transitions_ids = []
        for transition in self.transitions:
            if transition.is_doable():
                live_transitions_ids.append(transition.id)
        return live_transitions_ids

    def __get_live_transitions(self):
        live_transitions_ids = self.__get_live_transitions_ids()
        return [Helper.find_transition_by_id(self.transitions, id) for id in live_transitions_ids]

    def __get_reachability_graph(self):
        reachability_graph = ReachabilityGraph(self.transitions)
        return reachability_graph.get_graph()

    def __get_coverability_graph(self):
        coverability_graph = CoverabilityGraph(self.transitions)
        return coverability_graph.get_graph()

    def __get_places_k_bounded(self):
        states_list = CoverabilityGraph(self.transitions).get_graph()
        bounded_checker = BoundedChecker(states_list)
        return bounded_checker.get_places_k_bounded()

    def __is_network_k_bounded(self):
        states_list = CoverabilityGraph(self.transitions).get_graph()
        bounded_checker = BoundedChecker(states_list)
        return bounded_checker.is_network_k_bounded()

    def __is_network_safe(self):
        states_list = CoverabilityGraph(self.transitions).get_graph()
        bounded_checker = BoundedChecker(states_list)
        return bounded_checker.is_network_safe()

    def __is_network_conservative(self):
        states_list = CoverabilityGraph(self.transitions).get_graph()
        conservative_checker = ConservativeChecker(self.places, states_list)
        return conservative_checker.is_network_conservative()

    def __is_network_live(self):
        states_list = CoverabilityGraph(self.transitions).get_graph()
        liveness = LivenessChecker(self.transitions, states_list)
        return liveness.is_network_live()

    def __transitions_liveness(self):
        states_list = CoverabilityGraph(self.transitions).get_graph()
        liveness = LivenessChecker(self.transitions, states_list)
        return liveness.get_transitions_liveness()

    def __is_network_reversible(self):
        states_list = CoverabilityGraph(self.transitions).get_graph()
        reversibility_checker = ReversibilityChecker(states_list)
        return reversibility_checker.is_network_reversible()