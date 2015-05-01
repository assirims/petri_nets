import numpy


class Main(object):
    def __init__(self, places, transitions, connectors):
        self.places = places
        self.transitions = transitions
        self.connectors = connectors

    def __initialize_incidence_matrix(self):
        return numpy.zeros((len(self.places), len(self.transitions)))

    def __generate_ids(self, elements):
        for i in xrange(len(elements)):
            elements[i].id = i
        return elements

    def create_incidence_matrix(self):
        incidence_matrix_in = self.__initilize_incidene_matrix()
        incidence_matrix_out = self.__initilize_incidene_matrix()

        # objects in python are passed by reference
        self.__generate_ids(self.transitions)
        self.__generate_ids(self.places)

        for transition in self.transitions:
            for connector_in in transition.connectors_in:
                incidence_matrix_in[connector_in.place.id][transition.id] = connector_in.weight

            for connector_out in transition.connectors_out:
                incidence_matrix_out[connector_out.place.id][transition.id] = connector_out.weight

        return incidence_matrix_in - incidence_matrix_out