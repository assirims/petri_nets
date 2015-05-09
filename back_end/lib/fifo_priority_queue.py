from lib.exceptions import EmptyQueueError


class FifoPriorityQueue(object):

    def __init__(self):
        self.queue = []

    # override __cmp__() method in item object
    # here we can do some optimizations e.g. binary search
    def put(self, item):
        index = len(self.queue)

        for el in self.queue:
            if item < el:
                index = self.queue.index(el)
                break
        self.queue.insert(index, item)

    def get(self):
        try:
            return self.queue.pop(0)
        except IndexError:
            raise EmptyQueueError()

    def is_empty(self):
        return not self.queue

    def __len__(self):
        return len(self.queue)