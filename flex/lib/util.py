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


def str_to_bool (s):
    """
    Given a string, parses out whether it is meant to be True or not
    """
    s = str(s).lower()  # Make sure
    if s in ['true', 't', 'yes', 'y', 'on', 'enable', 'enabled', 'ok',
             'okay', '1', 'allow', 'allowed']:
        return True
    try:
        r = 10
        if s.startswith("0x"):
            s = s[2:]
            r = 16
        i = int(s, r)
        if i != 0:
            return True
    except:
        pass
    return False
