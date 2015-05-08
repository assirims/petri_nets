import uuid
import json


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
    def is_doable(self):
        for connector in self.connectors_in:
            if connector.weight > connector.place.tokens:
                return False
        return True

    def run_transition(self):
        if self.is_doable():
            for connector_in in self.connectors_in:
                connector_in.place.tokens = connector_in.place.tokens - connector_in.weight

            for connector_out in self.connectors_out:
                connector_out.place.tokens = connector_out.place.tokens + connector_out.weight

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)