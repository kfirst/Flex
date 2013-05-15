'''
Created on 2013-5-15

@author: kfirst
'''

from flex.model.match import DataMatch
from flex.base.module import Module


class MatchApi(Module):

    def data_match(self, data, port = None):
        return DataMatch(data, port)
