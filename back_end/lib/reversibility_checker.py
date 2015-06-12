from copy import deepcopy

# TODO: it doesn't work
class ReversibilityChecker(object):
    def __init__(self, states_list):
        self.states_list = deepcopy(states_list)

    def fun(self):
        for state in self.states_list:
            pass

    def __find_children(self, parent_state):
        children_ids = []
        for state in self.states_list:
            if state[1] == parent_state[0] and state[0] != parent_state[1]:
                parent_state[2][state[0]] = state[3]
                # children_ids.append(state.id)

        # return children_ids.extend([id for id in parent_state[2]])
