import unittest
from main import Main
from models.link import Connector, Direction
from models.place import Place
from models.transition import Transition


class TestTransitions(unittest.TestCase):
 
    def setUp(self):
        self.p1 = Place(name='p1', id=1, tokens=1)
        self.p2 = Place(name='p2', id=2, tokens=0)
        self.c1 = Connector(1, self.p1, Direction.PLACE_TO_TRANSITION, 1)
        self.c2 = Connector(2, self.p2, Direction.TRANSITION_TO_PLACE, 1)
        self.c3 = Connector(3, self.p2, Direction.PLACE_TO_TRANSITION, 1)
        self.t1 = Transition([self.c1], [self.c2], 1, id=1, name='t1')
        self.t2 = Transition([self.c3], [], 1, id=2, name='t2')
        self.main = Main([self.p1, self.p2], [self.t1, self.t2], [self.c1, self.c2])
 
    def test_proper_tokens_setup(self):
        self.assertEqual(self.p1.tokens, 1)
        self.assertEqual(self.p2.tokens, 0)
 
    def test_run_simple_transition(self):
        self.main.simulate()
        self.assertEqual(self.p1.tokens, 0)
        self.assertEqual(self.p2.tokens, 1)

if __name__ == '__main__':
    unittest.main()