'''
Created on 2013-5-15

@author: kfirst
'''

from flex.lib.util import object_to_string


class Action(object):

    OUTPUT = 1

    DESERIALIZER = {}

    def __init__(self, type):
        self.type = type

    @classmethod
    def deserialize(cls, data):
        deserializer = cls.DESERIALIZER[data[0]]
        return deserializer.deserialize(data)


class OutputAction(Action):

    def __init__(self, port):
        super(OutputAction, self).__init__(Action.OUTPUT)
        self.port = port

    def serialize(self):
        return (self.type, self.port)

    @classmethod
    def deserialize(cls, data):
        return cls(data[1])

    def __repr__(self):
        return object_to_string(self,
                    port = self.port)

Action.DESERIALIZER = {
    Action.OUTPUT: OutputAction,
}
