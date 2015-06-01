class ReversibilityChecker(object):
    def __init__(self, states_list):
        self.states_list = states_list

    def fun(self):
        for state in self.states_list:
            pass

    def __find_children(self, parent_id):
        children_ids = []
        for state in self.states_list:
            if state[1] == parent_id and state[0] != parent_id:
                children_ids.append(state.id)
            self.states_list[2][state[1]] = state[3]