import numpy


class IncidenceMatrixCreator(object):
    def __init__(self, places, transitions, links):
        self.places = places
        self.transitions = transitions
        self.links = links

    def __initialize_incidence_matrix(self):
        return numpy.zeros((len(self.places), len(self.transitions)))

    def create_incidence_matrix(self):
        incidence_matrix_in = self.__initialize_incidence_matrix()
        incidence_matrix_out = self.__initialize_incidence_matrix()

        for transition in self.transitions:
            for link_out in transition.links_out:
                incidence_matrix_in[link_out.place.id-1][transition.id-1] = link_out.weight

            for link_in in transition.links_in:
                incidence_matrix_out[link_in.place.id-1][transition.id-1] = link_in.weight

        return incidence_matrix_in - incidence_matrix_out