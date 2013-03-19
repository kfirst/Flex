# encoding: utf-8
'''
配置文件
Created on 2013-3-19

@author: kfirst
'''

import json
import os

class Config(object):
    '''
    配置文件，使用json格式存储，初始化时需要给定配置文件的路径
    '''

    ERR_PREFIX = 'Config: '

    def __init__(self, path):
        content = self._read_file(path)
        self._config = self._parse_content(content)

    def _read_file(self, path):
        try:
            fd = open(path)
        except IOError:
            self._err('The config file \'' + path + '\' is not found!')
        content = ''
        for line in fd:
            content += line
        fd.close()
        return content

    def _parse_content(self, content):
        try:
            return json.loads(content)
        except ValueError:
            self._err('The format of the config file is not correct! Json format is accepted.')

    def _err(self, info):
        print self.ERR_PREFIX + info
        os.abort()

    '''
    获取配置文件中指定key的值，key可以为多级，用‘.’分隔，如：
    get('log.level')与get('log')['level']的返回值是一样的
    '''
    def get(self, key, default = None):
        keys = key.split('.')
        value = self._config
        try:
            for k in keys:
                value = value[k]
            return value
        except KeyError:
            if default is None:
                self._err('The key \'' + k + '\' in \'' + key + '\' is not found in config!')
            return default


if __name__ == '__main__':
    config = Config('../../config')
    print config.get('log.level')
    print config.get('log')['level']


