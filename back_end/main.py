from lib.exceptions import EmptyQueueError
from lib.fifo_priority_queue import FifoPriorityQueue
from models.connector import Connector, Direction
from models.place import Place
from models.transition import Transition


class Main(object):

    START = 1
    SIMULATE = 2
    GRAPH_FEATURES = 3
    END = 4

    def __init__(self, places, transitions, connectors):
        self.places = places
        self.transitions = transitions
        self.connectors = connectors

    def __json_type_wrapper(self, type, data=None):
        content = {"type": type, "data": data}
        return '{"type": %s, "data": %s}' % (type, data)

    def start_simulation(self):
        return '{"type": %s, "data": ""}' % Main.START

    def simulate(self):
        self.queue = FifoPriorityQueue()
        for transition in self.transitions:
            if transition.is_doable():
                self.queue.put(transition)

        try:
            transition = self.queue.get()
            # print transition.name
            transition.run_transition()
            return self.__json_type_wrapper(Main.SIMULATE, transition.to_json())
        except EmptyQueueError:
            return self.__json_type_wrapper(Main.END)

# Example data needed for faster development process
#
# p1 = Place(name='p1', id=1, tokens=1)
# p2 = Place(name='p2', id=2, tokens=0)
# p3 = Place(name='p3', id=3, tokens=1)
# p4 = Place(name='p4', id=4, tokens=0)
# c1 = Connector(1, p1, Direction.PLACE_TO_TRANSITION, 1)
# c2 = Connector(2, p2, Direction.TRANSITION_TO_PLACE, 1)
# c3 = Connector(3, p2, Direction.PLACE_TO_TRANSITION, 1)
# c4 = Connector(4, p1, Direction.TRANSITION_TO_PLACE, 1)
# c5 = Connector(5, p3, Direction.TRANSITION_TO_PLACE, 2)
# c6 = Connector(6, p3, Direction.PLACE_TO_TRANSITION, 1)
# c7 = Connector(7, p4, Direction.TRANSITION_TO_PLACE, 3)
# t1 = Transition([c1], [c2], 5, id=1, name='t1')
# t2 = Transition([c3], [c4, c5], 1, id=2, name='t2')
# t3 = Transition([c6], [c7], 2, id=3, name='t3')
# #
# main = Main([p1, p2, p3, p4], [t1, t2, t3], [c1, c2, c3, c4, c5, c6, c7])
# print main.places[0].tokens
# print main.places[1].tokens
#
# print main.simulate()
# # print main.places[0].tokens
# # print main.places[1].tokens
#
# print main.simulate()
# # print main.places[0].tokens
# # print main.places[1].tokens
# print main.simulate()
# print main.simulate()
# print main.simulate()
# print main.simulate()
# print main.simulate()