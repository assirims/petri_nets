from lib.exceptions import EmptyQueueError
from lib.fifo_priority_queue import FifoPriorityQueue
from models.connector import Connector, Direction
from models.place import Place
from models.transition import Transition


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

        try:
            transition = self.queue.get()
            transition.run_transition()
            return transition.to_json()
        except EmptyQueueError:
            return 'Simulation has been finished.'


p1 = Place(name='p1', id=1, tokens=1)
p2 = Place(name='p2', id=2, tokens=0)
c1 = Connector(p1, Direction.PLACE_TO_TRANSITION, 1)
c2 = Connector(p2, Direction.TRANSITION_TO_PLACE, 1)
c3 = Connector(p2, Direction.PLACE_TO_TRANSITION, 1)
c4 = Connector(p1, Direction.TRANSITION_TO_PLACE, 1)
t1 = Transition([c1], [c2], 1, id=1, name='t1')
t2 = Transition([c3], [c4], 1, id=2, name='t2')

main = Main([p1,p2], [t1, t2], [c1,c2,c3,c4])
print main.places[0].tokens
print main.places[1].tokens

print main.simulate()
print main.places[0].tokens
print main.places[1].tokens

print main.simulate()
print main.places[0].tokens
print main.places[1].tokens

print 'lolku'
