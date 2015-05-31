from lib.exceptions import EmptyStatesListError


class BoundedChecker(object):

    def __init__(self, states_list):
        self.__find_places_k_bounded(states_list)

    def __find_places_k_bounded(self, states_list):
        try:
            self.places_k_bounded = [0 for i in xrange(len(states_list[0][2]))]
            for state in states_list:
                for i in xrange(len(state[2])):
                    if self.places_k_bounded[i] < state[2][i]:
                        self.places_k_bounded[i] = state[2][i]

            return self.places_k_bounded
        except IndexError:
            raise EmptyStatesListError()

    def get_places_k_bounded(self):
        return self.places_k_bounded

    def is_network_k_bounded(self):
        return self.places_k_bounded == [self.places_k_bounded[0] for token in xrange(len(self.places_k_bounded)-1)] \
            and self.places_k_bounded[0] != float("inf")

    def is_network_safe(self):
        return self.places_k_bounded == [1 for token in xrange(len(self.places_k_bounded)-1)]
