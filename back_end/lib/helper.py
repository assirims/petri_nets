from utils.fifo_priority_queue import FifoPriorityQueue


class Helper(object):
    @staticmethod
    def generate_ids(elements):
        for i in xrange(len(elements)):
            elements[i].id = i
        return elements

    @staticmethod
    def find_state_by_id(states, id):
        for state in states:
            if state[0] == id:
                return state

    @staticmethod
    def find_place_by_id(places, id):
        return Helper.find_element_by_id(places, id)

    @staticmethod
    def find_link_by_id(links, id):
        return Helper.find_element_by_id(links, id)

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
            for link_in in transition.links_in:
                if link_in.place is place:
                    transitions_with_place.append(transition)
        return transitions_with_place

    @staticmethod
    def get_competitive_transitions_priority_queue(transitions, transition):
        priority_queue = FifoPriorityQueue()
        priority_queue.put(transition)

        links_in = transition.links_in
        places_in = [conn_in.place for conn_in in links_in]
        for place in places_in:
            for trans in Helper.get_transitions_with_input_place(transitions, place):
                if trans.is_doable():
                    priority_queue.put(trans)

        return priority_queue