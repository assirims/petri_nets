class ConservativeChecker(object):
    def __init__(self, states_list):
        self.states_list = states_list

    def is_network_conservative(self):
        start_marking_sum = sum(self.states_list[0][2])
        for state in self.states_list:
            if sum(state[2]) != start_marking_sum:
                return False
        return True