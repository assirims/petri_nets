from lib.fifo_priority_queue import FifoPriorityQueue


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

    @staticmethod
    def get_transitions_with_input_place(transitions, place):
        transitions_with_place = []
        for transition in transitions:
            for connector_in in transition.connectors_in:
                if connector_in.place is place:
                    transitions_with_place.append(transition)
        return transitions_with_place

    @staticmethod
    def get_competitive_transitions_priority_queue(transitions, transition):
        priority_queue = FifoPriorityQueue()
        priority_queue.put(transition)

        connectors_in = transition.connectors_in
        places_in = [conn_in.place for conn_in in connectors_in]
        for place in places_in:
            for trans in Helper.get_transitions_with_input_place(transitions, place):
                if trans.is_doable():
                    priority_queue.put(trans)

        return priority_queue