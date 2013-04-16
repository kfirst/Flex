'''
Created on 2013-3-29

@author: kfirst
'''

def object_to_string(obj, *args, **kwargs):
    s = obj.__class__.__name__
    para = []
    for value in args:
        para.append(value.__str__())
    for key in kwargs:
        para.append(key + ': ' + kwargs[key].__str__())
    return s + '(' + ', '.join(para) + ')'


def parse_packet(packet_data):
    from pox.lib.packet.ethernet import ethernet
    return ethernet(packet_data)
