'''
Created on 2013-5-15

@author: kfirst
'''

from flex.lib.util import object_to_string


class Match(object):

    DATA = 1

    DESERIALIZER = {}

    def __init__(self, type):
        self.type = type

    @classmethod
    def deserialize(cls, data):
        deserializer = cls.DESERIALIZER[data[0]]
        return deserializer.deserialize(data)


class DataMatch(Match):

    def __init__(self, data, port):
        super(DataMatch, self).__init__(Match.DATA)
        self.data = data
        self.port = port

    def serialize(self):
        return (self.type, self.data, self.port)

    @classmethod
    def deserialize(cls, data):
        return cls(data[1], data[2])

    def __repr__(self):
        return object_to_string(self)


Match.DESERIALIZER = {
    Match.DATA: DataMatch,
}
