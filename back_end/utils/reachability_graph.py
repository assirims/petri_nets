from copy import deepcopy
from utils.helper import Helper


class ReachabilityGraph(object):
    def __init__(self, transitions):
        self.transitions = deepcopy(transitions)

    # states_list contains tuples: (id_state, parent_id_state, [net states])
    def _create_reachability_graph(self):
        queue = [(0, 0, self.transitions)]
        states_list = [(0, 0, self._get_network_state(self.transitions), [])]
        stop_condition = 10
        state_id = 0
        while queue and state_id < stop_condition:
            state = queue.pop(0)
            parent_state_id = state[0]
            transitions = state[2]

            transitions_ids_to_do = []
            for transition in transitions:
                if transition.is_doable():
                    priority_queue = Helper.get_competitive_transitions_priority_queue(transitions, transition)
                    if priority_queue.get() is transition:
                        transitions_ids_to_do.append(transition.id)

            for transition_id in transitions_ids_to_do:
                new_transitions_state = deepcopy(transitions)
                transition = Helper.find_transition_by_id(new_transitions_state, transition_id)
                transition.run_transition()
                new_network_state = self._get_network_state(new_transitions_state)
                found_state = self.find_state_based_on_network_state(states_list, new_network_state)

                if found_state is not None:
                    id = found_state[0]
                    parent_network_state = self.find_state_based_on_transitions(states_list, transitions)
                    parent_network_state[3].append(id)
                else:
                    state_id += 1
                    states_list.append((state_id, parent_state_id, new_network_state, []))
                    queue.append((state_id, parent_state_id, new_transitions_state))

        return states_list

    def find_state_based_on_network_state(self, states_list, new_network_state):
        for state in states_list:
            if state[2] == new_network_state:
                return state
        return None

    def find_state_based_on_transitions(self, states_list, transitions):
        for state in states_list:
            if state[2] == self._get_network_state(transitions):
                return state
        return None

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

    def get_reachability_graph(self):
        return self._create_reachability_graph()