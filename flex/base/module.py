# encoding: utf-8
'''
Created on 2013-3-27

@author: kfirst
'''

class Module(object):
    '''
    所有模块的基类
    '''

    def start(self):
        '''
        模块必须实现的方法，用于和其他模块交互。
        每个模块的初始化方法中，除config、logger、event模块外不能调用其他的模块，因为无法预知core中模块的载入顺序，
        如有调用其他模块、或者启动线程等操作，需要在该方法中完成。
        core会在所有模块载入完毕后调用各个模块的start方法。
        '''
        pass

    def terminate(self):
        '''
        模块关闭时调用的方法，用于释放资源或者其他必要的操作
        '''
        pass
