import numpy
from utils.helper import Helper


class IncidenceMatrixCreator(object):
    def __init__(self, places, transitions, connectors):
        self.places = places
        self.transitions = transitions
        self.connectors = connectors

    def __initialize_incidence_matrix(self):
        return numpy.zeros((len(self.places), len(self.transitions)))

    def create_incidence_matrix(self):
        incidence_matrix_in = self.__initialize_incidence_matrix()
        incidence_matrix_out = self.__initialize_incidence_matrix()

        for transition in self.transitions:
            for connector_out in transition.connectors_out:
                incidence_matrix_in[connector_out.place.id-1][transition.id-1] = connector_out.weight

            for connector_in in transition.connectors_in:
                incidence_matrix_out[connector_in.place.id-1][transition.id-1] = connector_in.weight

        return incidence_matrix_in - incidence_matrix_out