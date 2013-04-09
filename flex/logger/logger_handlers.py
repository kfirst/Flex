'''
Created on 2013-4-9

@author: kfirst
'''
from logging import StreamHandler

class ColorStreamHandler(StreamHandler):

    def __init__(self):
        super(ColorStreamHandler, self).__init__()
        old_format = self.format
        def new_format (record):
            msg = _proc(old_format(record), record.levelname)
            color = LEVEL_COLORS.get(record.levelname)
            if color is None:
                return msg
            return _color(color, msg)
        self.format = new_format


_strip_only = False

# Control Sequence Introducer
CSI = "\033["

# Magic sequence used to introduce a command or color
MAGIC = "@@@"

# Colors for log levels
LEVEL_COLORS = {
    'DEBUG': 'CYAN',
    'INFO': 'GREEN',
    'WARNING': 'YELLOW',
    'ERROR': 'RED',
    'CRITICAL': 'blink@@@RED',
}

# Name to (intensity, base_value) (more colors added later)
COLORS = {
    'black' : (0, 0),
    'red' : (0, 1),
    'green' : (0, 2),
    'yellow' : (0, 3),
    'blue' : (0, 4),
    'magenta' : (0, 5),
    'cyan' : (0, 6),
    'gray' : (0, 7),
    'darkgray' : (1, 0),
    'pink' : (1, 1),
    'white' : (1, 7),
}

# Add intense/bold colors (names it capitals)
for _c in [_n for _n, _v in COLORS.items() if _v[0] == 0]:
    COLORS[_c.upper()] = (1, COLORS[_c][1])

COMMANDS = {
    'reset' : 0,
    'bold' : 1,
    'dim' : 2,
    'bright' : 1,
    'dull' : 2,
    'bright:' : 1,
    'dull:' : 2,
    'blink' : 5,
    'BLINK' : 6,
    'invert' : 7,
    'bg:' :-1,  # Special
    'level' :-2,  # Special -- color of current level
    'normal' : 22,
    'underline' : 4,
    'nounderline' : 24,
}

def _color (color, msg):
  """ Colorizes the given text """
  return _proc(MAGIC + color) + msg + _proc(MAGIC + 'reset').lower()

def _proc (msg, level_color = "DEBUG"):
  """
  Do some replacements on the text
  """
  msg = msg.split(MAGIC)
  # print "proc:",msg
  r = ''
  i = 0
  cmd = False
  while i < len(msg):
    m = msg[i]
    # print i,m
    i += 1
    if cmd:
      best = None
      bestlen = 0
      for k, v in COMMANDS.iteritems():
        if len(k) > bestlen:
          if m.startswith(k):
            best = (k, v)
            bestlen = len(k)
      special = None
      if best is not None and best[0].endswith(':'):
        special = best
        m = m[bestlen:]
        best = None
        bestlen = 0
      for k, v in COLORS.iteritems():
        if len(k) > bestlen:
          if m.startswith(k):
            best = (k, v)
            bestlen = len(k)
      if best is not None:
        # print "COMMAND", best
        m = m[bestlen:]
        if type(best[1]) is tuple:
          # Color
          brightness, color = best[1]
          if special is not None:
            if special[1] == -1:
              brightness = None
              color += 10
          color += 30
          if not _strip_only:
            r += CSI
            if brightness is not None:
              r += str(brightness) + ";"
            r += str(color) + "m"
        elif not _strip_only:
          # Command
          if best[1] == -2:
            r += _proc(MAGIC + LEVEL_COLORS.get(level_color, ""), level_color)
          else:
            r += CSI + str(best[1]) + "m"
    cmd = True
    r += m
  return r
