# -*- coding: utf-8 -*-
from copy import deepcopy
from lib.graph import Graph
from lib.helper import Helper


class CoverabilityGraph(Graph):
    # states_list contains tuples: (id_state, parent_id_state, [net states], {state_id: transition_id}, transition_id)
    def _create_coverability_graph(self):
        queue = [(0, 0, self.transitions)]
        states_list = [(0, 0, self._get_network_state(self.transitions), {}, None)]
        stop_condition = 20
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

                state_id += 1
                states_list_element = (state_id, parent_state_id, new_network_state, {}, transition.id)

                predecessors = self._get_predecessors(states_list, states_list_element)
                self._check_infinite_state(predecessors, new_network_state)
                found_state = self._find_state_based_on_network_state(states_list, new_network_state)

                if found_state is not None:
                    state_id -= 1
                    id = found_state[0]
                    parent_network_state = self._find_state_by_id(states_list, parent_state_id)
                    parent_network_state[3][id] = transition.id
                else:
                    states_list.append(states_list_element)
                    queue.append((state_id, parent_state_id, new_transitions_state))

        return states_list

    def _get_predecessors(self, states_list, state):
        predecessors_list = []
        state_id = state[0]
        parent_id = state[1]
        finish = False
        while not (state_id == 0 and finish is True):
            if state_id == 0:
                finish = True
            parent = self._find_state_by_id(states_list, parent_id)

            if state_id != 0:
                predecessors_list.append(parent)

            parent_id = parent[1]
            state_id = parent[0]

        return predecessors_list

    def _check_infinite_state(self, predecessors, network_state):
        for predecessor in predecessors:
            if predecessor[2] != network_state:
                exist = True
                for i in xrange(len(predecessor[2])):
                    if predecessor[2][i] > network_state[i] and predecessor[2][i] != float("inf"):
                        exist = False
                        break
                if exist:
                    for i in xrange(len(predecessor[2])):
                        if predecessor[2][i] < network_state[i] or predecessor[2][i] == float("inf"):
                            network_state[i] = float("inf")
                    break

    def get_graph(self, parsed_inf=False):
        coverability_graph = self._create_coverability_graph()
        if parsed_inf:
            for state in coverability_graph:
                for index, token in enumerate(state[2]):
                    if token == float("inf"):
                        state[2][index] = "∞"

        return coverability_graph