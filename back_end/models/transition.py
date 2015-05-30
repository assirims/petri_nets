import uuid
import json


class Transition(object):
    def __init__(self, links_in, links_out, priority, id=None, name=uuid.uuid4().get_hex()):
        self.links_in = links_in
        self.links_out = links_out
        self.priority = priority
        self.id = id
        self.name = name

    # used by FifoPriorityQueue
    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

    # check that you can execute transition
    def is_doable(self):
        for link in self.links_in:
            if link.weight > link.place.tokens:
                return False
        return True

    def run_transition(self):
        if self.is_doable():
            for link_in in self.links_in:
                link_in.place.tokens = link_in.place.tokens - link_in.weight

            for link_out in self.links_out:
                link_out.place.tokens = link_out.place.tokens + link_out.weight

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)