class CoverabilityGraphElement(object):
    def __init__(self, id, parent_id, graph_representation, coverability_graph):
        self.id = id
        self.parent_id = parent_id
        self.graph_representation = graph_representation
        self.duplicated = self.__is_duplicated(coverability_graph)

    def __is_duplicated(self, coverability_graph):
        for element in coverability_graph:
            if element.graph_representation == self.graph_representation:
                return True
        return False