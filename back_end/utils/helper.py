class Helper(object):
    @staticmethod
    def generate_ids(elements):
        for i in xrange(len(elements)):
            elements[i].id = i
        return elements

    @staticmethod
    def find_place_by_id(places, id):
        return Helper.find_element_by_id(places, id)

    @staticmethod
    def find_connector_by_id(connectors, id):
        return Helper.find_element_by_id(connectors, id)

    @staticmethod
    def find_transition_by_id(transitions, id):
        return Helper.find_element_by_id(transitions, id)

    @staticmethod
    def find_element_by_id(elements, id):
        for element in elements:
            if element.id == id:
                return element