import uuid


class Place(object):
    def __init__(self, name=uuid.uuid4().get_hex(), id=None, tokens=0):
        self.id = id
        self.name = name
        self.tokens = tokens