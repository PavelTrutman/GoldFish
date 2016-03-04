#!/usr/bin/python3

import os
import shutil
import time
import math


def readableSize(bytes):
  suffixes = ['B', 'KB', 'MB', 'GB', 'TB']

  if bytes:
    order = int(math.log2(bytes) / 10)
    return '{:7.2f} {}'.format(bytes / (1 << order * 10), suffixes[order])
  else:
    return '   0.00 B'




backupDirTo = '/backupDirTo'
backupDirFrom = ['/backupDirFrom']

prevBackups = list(reversed(os.listdir(backupDirTo)))

today = time.strftime('%Y%m%d_%H%M')
dirToday = os.path.join(backupDirTo, today)
os.mkdir(dirToday)

print('Creating new backup: ' + today)

for dirFrom in backupDirFrom:
  backupDir = os.path.basename(dirFrom)
  dirTo = os.path.join(dirToday, backupDir)
  os.mkdir(dirTo)

  #find prev backup
  dirPrev = None
  datePrev = None
  for prev in prevBackups:
    dirPrevTmp = os.path.join(backupDirTo, prev, backupDir)
    if os.path.isdir(dirPrevTmp):
      dirPrev = dirPrevTmp
      datePrev = prev
      break
  
  print()
  print(backupDir)
  print('  From: ' + dirFrom)
  print('  To:   ' + dirTo)
  if datePrev is None:
    print('  No previous backup found.')
  else:
    print('  Previous backup found from: ' + datePrev)
  
  sizeCopied = 0
  sizeLinked = 0
 
  for root, dirs, files in os.walk(dirFrom):
    relPath = os.path.relpath(root, dirFrom)
    curDirTo = os.path.join(dirTo, relPath)
    for dir in dirs:
      os.mkdir(os.path.join(curDirTo, dir))
    for file in files:
      fileFrom = os.path.join(root, file)
      fileTo = os.path.join(curDirTo, file)
      copied = False
      if not (dirPrev is None):
        filePrev = os.path.join(dirPrev, relPath, file)
        if os.path.isfile(filePrev):
          statFrom = os.stat(fileFrom)
          statPrev = os.stat(filePrev)
          if (statFrom.st_size == statPrev.st_size) and (round(statFrom.st_mtime) == round(statPrev.st_mtime)):
            os.link(filePrev, fileTo)
            copied = True
            sizeLinked += statFrom.st_size
      if not copied:
        shutil.copy2(fileFrom, fileTo)
        print('    ' + os.path.join(relPath, file))
        sizeCopied += os.stat(fileFrom).st_size
  print('  Copied: ' + readableSize(sizeCopied))
  print('  Linked: ' + readableSize(sizeLinked))

