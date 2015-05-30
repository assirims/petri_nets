class Direction(object):
    PLACE_TO_TRANSITION = 0
    TRANSITION_TO_PLACE = 1


class Connector(object):
    def __init__(self, id, place, direction, weight):
        self.id = id
        self.place = place
        self.direction = direction
        self.weight = weight