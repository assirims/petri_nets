class Direction(object):
    PLACE_TO_TRANSITION = 1
    TRANSITION_TO_PLACE = 2


class Connector(object):
    def __init__(self, place, direction, weight):
        self.place = place
        self.direction = direction
        self.weight = weight