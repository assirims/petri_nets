from copy import deepcopy
from utils.helper import Helper


class CoverabilityGraph(object):
    def __init__(self, transitions):
        self.transitions = deepcopy(transitions)

    def _create_coverability_graph(self):
        queue = [self.transitions]
        states_list = [self._get_network_state(self.transitions)]
        stop_condition = 100
        i = 0
        while queue and i < stop_condition:
            i += 1
            transitions = queue.pop(0)
            transitions_ids_to_do = []
            for transition in transitions:
                if transition.is_doable():
                    transitions_ids_to_do.append(transition.id)

            for transition_id in transitions_ids_to_do:
                new_transitions_state = deepcopy(transitions)
                transition = Helper.find_transition_by_id(new_transitions_state, transition_id)
                transition.run_transition()
                states_list.append(self._get_network_state(new_transitions_state))
                queue.append(new_transitions_state)

        return states_list

    def _get_network_state(self, transitions):
        places_ids_and_tokens = {}
        for transition in transitions:
            for conn_in in transition.connectors_in:
                if conn_in.place.id not in places_ids_and_tokens:
                    places_ids_and_tokens[conn_in.place.id] = conn_in.place.tokens

            for conn_out in transition.connectors_out:
                if conn_out.place.id not in places_ids_and_tokens:
                    places_ids_and_tokens[conn_out.place.id] = conn_out.place.tokens

        return [token for token in places_ids_and_tokens.values()]

    def get_coverability_graph(self):
        return self._create_coverability_graph()