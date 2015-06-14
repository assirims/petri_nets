from copy import deepcopy
from abc import ABCMeta, abstractmethod


class Graph(object):
    __metaclass__ = ABCMeta

    def __init__(self, transitions):
        self.transitions = deepcopy(transitions)

    def _find_state_based_on_network_state(self, states_list, new_network_state):
        for state in states_list:
            if state[2] == new_network_state:
                return state
        return None

    def _find_state_based_on_transitions(self, states_list, transitions):
        for state in states_list:
            if state[2] == self._get_network_state(transitions):
                return state
        return None

    def _find_state_by_id(self, states_list, state_id):
        for state in states_list:
            if state[0] == state_id:
                return state
        return None

    def _get_network_state(self, transitions):
        places_ids_and_tokens = {}
        for transition in transitions:
            for conn_in in transition.links_in:
                if conn_in.place.id not in places_ids_and_tokens:
                    places_ids_and_tokens[conn_in.place.id] = conn_in.place.tokens

            for conn_out in transition.links_out:
                if conn_out.place.id not in places_ids_and_tokens:
                    places_ids_and_tokens[conn_out.place.id] = conn_out.place.tokens

        return [token for token in places_ids_and_tokens.values()]

    @abstractmethod
    def get_graph(self,parsed_inf=False):
        pass
