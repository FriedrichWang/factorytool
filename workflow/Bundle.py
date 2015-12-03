__author__ = 'friedrich'


class Bundle(object):

    def __init__(self):
        self.id = ""
        self.tag = ""
        self.params = {}

    def clear(self):
        self.params = {}
