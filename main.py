from lib.fifo_priority_queue import FifoPriorityQueue


class Main(object):

    def __init__(self, places, transitions, connectors):
        self.places = places
        self.transitions = transitions
        self.connectors = connectors

    def simulate(self):
        self.queue = FifoPriorityQueue()
        for transition in self.transitions:
            if transition.is_doable():
                self.queue.put(transition)

        self.queue.get().run_transition()
