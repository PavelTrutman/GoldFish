#!/usr/bin/python3

import shutil
import math
import sys
import re
import hashlib

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


def queryYesNo(question, default=None):
  """
  Asks a yes/no question via raw_input() and return their answer.

  Args:
    question (str): a string that is presented to the user
    default (str): the presumed answer if the user just hits <Enter>. It must be 'yes', 'no' or None (default) (meaning an answer is required of the user)

  Returns:
    bool: True for 'yes' or False for 'no'
  """

  valid = {'yes': True, 'y': True, 'no': False, 'n': False}
  if default is None:
    prompt = ' [y/n] '
  elif default == 'yes':
    prompt = ' [Y/n] '
  elif default == 'no':
    prompt = ' [y/N] '
  else:
    raise ValueError('Invalid default answer: {}'.format(default))

  while True:
    sys.stdout.write(question + prompt)
    choice = input().lower()
    if default is not None and choice == '':
      return valid[default]
    elif choice in valid:
      return valid[choice]


def hashFile(path):
  """
  Compute the SHA256 hash of the file.

  Args:
    path (str): path to the file

  Returns:
    str: hash of the file
  """

  fileHash = hashlib.sha256()
  with open(path, 'rb') as f:
    while True:
      data = f.read(65536)
      if not data:
        break
      fileHash.update(data)

  return fileHash.hexdigest()
