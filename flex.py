#!/usr/bin/env python
'''
Created on 2013-4-7

@author: kfirst
'''

''''true
export OPT="-u -O"
export FLG=""
if [ "$(basename $0)" = "debug-pox.py" ]; then
  export OPT=""
  export FLG="--debug"
fi

if [ -x pypy/bin/pypy ]; then
  exec pypy/bin/pypy $OPT "$0" $FLG "$@"
fi

if type python2.7 > /dev/null; then
  exec python2.7 $OPT "$0" $FLG "$@"
fi
exec python $OPT "$0" $FLG "$@"
'''

from flex.core import core
import sys
import time

try:
    config_path = sys.argv[1]
except IndexError:
    config_path = 'config'

core.set_config_path(config_path)
core.start()

try:
    while True:
        time.sleep(10)
except:
    pass

core.terminate()
