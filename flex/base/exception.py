# encoding: utf-8
'''
各种Exception
Created on 2013-3-29

@author: fzm
'''

class ControllerNotFoundException(Exception):
    pass


class SwitchNotFoundException(Exception):
    pass


class ConnectFailException(Exception):
    pass


class IllegalKeyException(Exception):
    pass
