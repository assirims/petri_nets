class Helper(object):
    @staticmethod
    def generate_ids(elements):
        for i in xrange(len(elements)):
            elements[i].id = i
        return elements

    @staticmethod
    def find_place_by_id(places, id):
        for place in places:
            if place.id == id:
                return place

    @staticmethod
    def find_connector_by_id(connectors, id):
        for connector in connectors:
            if connector.id == id:
                return connector