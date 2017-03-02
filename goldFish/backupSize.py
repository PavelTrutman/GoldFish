#!/usr/bin/python3

import os
import shutil
import time
import math
import sys
import re
from .os import *


if __name__ == '__main__':
  
  dirFrom = str(sys.argv[1])

  printHeadline()
  print('Folder to inspect:' + dirFrom)
  sizeTotal = 0
  sizeDelete = 0
 
  for root, dirs, files in os.walk(dirFrom):
    relPath = os.path.relpath(root, dirFrom)
    for file in files:
      fileFrom = os.path.join(root, file)
      printToTerminalSize(os.path.join(relPath, file))
      sys.stdout.flush()

      statFrom = os.stat(fileFrom)
      if statFrom.st_nlink == 1:
        sizeDelete += statFrom.st_size
      sizeTotal += statFrom.st_size

      sys.stdout.write('\r')
      sys.stdout.flush()
      printToTerminalSize(' ')
      sys.stdout.write('\r')
      sys.stdout.flush()

  print('  Size of the backup:           ' + readableSize(sizeTotal))
  print('  Will be freed after deletion: ' + readableSize(sizeDelete))

