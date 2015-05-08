class Helper(object):
    @staticmethod
    def generate_ids(elements):
        for i in xrange(len(elements)):
            elements[i].id = i
        return elements