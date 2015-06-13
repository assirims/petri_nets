class ConservativeChecker(object):
    def __init__(self, places, states_list):
        self.places = places
        self.states_list = states_list

    def is_network_conservative(self, vector_coefficients=None):
        if not vector_coefficients:
            vector_coefficients = [1 for i in xrange(len(self.places))]

        root_state_sum = -1
        for state in self.states_list:
            states_tokens_sum = 0
            for i in xrange(len(state[2])):
                states_tokens_sum += state[2][i] * vector_coefficients[i]

            if root_state_sum == -1:
                root_state_sum = states_tokens_sum

            if states_tokens_sum != root_state_sum:
                return False
        return True