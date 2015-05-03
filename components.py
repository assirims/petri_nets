import uuid

class Direction(object):
    PLACE_TO_TRANSITION = 1
    TRANSITION_TO_PLACE = 2


class Place(object):
    def __init__(self, name=uuid.uuid4().get_hex(), id=None, tokens=0):
        self.id = id
        self.name = name
        self.tokens = tokens


class Transition(object):
    def __init__(self, connectors_in, connectors_out, priority, id=None, name=uuid.uuid4().get_hex()):
        self.connectors_in = connectors_in
        self.connectors_out = connectors_out
        self.priority = priority
        self.id = id
        self.name = name

    # used by FifoPriorityQueue
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

    # check that you can execute transition
    def __is_doable(self):
        for connector in self.connectors_in:
            if connector.weight > connector.place.tokens:
                return False
        return True

    def run_transition(self):
        if self.__is_doable():
            for connector_in in self.connectors_in:
                connector_in.place.tokens = connector_in.place.tokens - connector_in.weight

            for connector_out in self.connectors_out:
                connector_out.place.tokens = connector_out.place.tokens + connector_out.weight


class Connector(object):
    def __init__(self, place, direction, weight):
        self.place = place
        self.direction = direction
        self.weight = weight