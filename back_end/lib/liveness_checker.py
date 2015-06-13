class LivenessChecker(object):
    def __init__(self, transitions, states_list):
        self.transitions = transitions
        self.states_list = states_list

    def get_transitions_liveness(self):
        fired_transitions = []
        for state in self.states_list:
            transition = state[4]
            if transition != None:
                fired_transitions.append(state[4])

            for child_transition in state[3].values():
                fired_transitions.append(child_transition)

        fired_transitions = list(set(fired_transitions))
        return fired_transitions

    def is_network_live(self):
        return len(self.transitions) == len(self.get_transitions_liveness())