from copy import deepcopy
from lib.graph import Graph
from lib.helper import Helper


class ReachabilityGraph(Graph):
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
                found_state = self._find_state_based_on_network_state(states_list, new_network_state)

                if found_state is not None:
                    id = found_state[0]
                    parent_network_state = self._find_state_based_on_transitions(states_list, transitions)
                    parent_network_state[3].append(id)
                else:
                    state_id += 1
                    states_list.append((state_id, parent_state_id, new_network_state, []))
                    queue.append((state_id, parent_state_id, new_transitions_state))

        return states_list

    def get_graph(self):
        return self._create_reachability_graph()