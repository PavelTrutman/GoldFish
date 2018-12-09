#!/usr/bin/python3

import os
import sys
import pathlib
from .io import *

class Size:

  def main(path):
    """
    Get size of the backuped folder.

    Args:
      path (str): path to backuped folder

    Returns:
      None

    Throws:
      FileNotFoundError: when the folder does not exists
    """

    dirFrom = pathlib.Path(path)
    if not dirFrom.exists():
      raise FileNotFoundError(dirFrom)

    printHeadline()
    sizeTotal = 0
    sizeDelete = 0
   
    for root, dirs, files in os.walk(dirFrom):
      relPath = os.path.relpath(root, dirFrom)
      for file in files:
        fileFrom = os.path.join(root, file)
        printToTerminalSize(os.path.join(relPath, file))
        sys.stdout.flush()

        statFrom = os.stat(fileFrom, follow_symlinks=False)
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
