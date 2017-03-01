#!/usr/bin/python3

import shutil
import math
import sys
import re

def readableSize(bytes):
  """
  Converts bytes to kilobytes, megabytes, ...

  Args:
    bytes (int): size in bytes

  Returns:
    str: human readable size 
  """

  suffixes = ['B', 'KB', 'MB', 'GB', 'TB']

  if bytes:
    order = int(math.log2(bytes) / 10)
    return '{:7.2f} {}'.format(bytes / (1 << order * 10), suffixes[order])
  else:
    return '   0.00 B'


def printToTerminalSize(text):
  """
    Writes the given text to the standard terminal output. When the text is longer than the terminal size, the text is shorten to its size.

  Args:
    text (str): text to print

  Returns:
    None
  """

  width = shutil.get_terminal_size().columns
  half = int((width - 3)/2)
  if len(text) > width:
    text = re.sub(r'^(.{' + str(half) + '}).*(.{' + str(half) + '})$', '\g<1>...\g<2>', text)
  sys.stdout.write('{:{}.{}}'.format(text, 2*half + 3, 2*half + 3))


def printHeadline():
  """
  Prints the logo.

  Args:

  Returns:
    None
  """

  print(\
    '   _____       _     _ ______ _     _     \n'\
    '  / ____|     | |   | |  ____(_)   | |    \n'\
    ' | |  __  ___ | | __| | |__   _ ___| |__  \n'\
    ' | | |_ |/ _ \| |/ _` |  __| | / __| \'_ \ \n'\
    ' | |__| | (_) | | (_| | |    | \__ \ | | |\n'\
    '  \_____|\___/|_|\__,_|_|    |_|___/_| |_|\n'\
  )

