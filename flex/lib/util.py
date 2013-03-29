'''
Created on 2013-3-29

@author: kfirst
'''

def object_to_string(obj, *args, **kwargs):
    s = obj.__class__.__name__
    para = list(args)
    for key in kwargs:
        para.append(key + ': ' + kwargs[key].__str__())
    return s + '(' + ', '.join(para) + ')'

