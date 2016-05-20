#!/usr/bin/python3

import os
import shutil
import time
import math
import sys
import re


def readableSize(bytes):
  suffixes = ['B', 'KB', 'MB', 'GB', 'TB']

  if bytes:
    order = int(math.log2(bytes) / 10)
    return '{:7.2f} {}'.format(bytes / (1 << order * 10), suffixes[order])
  else:
    return '   0.00 B'

def printToTerminalSize(text):
  width = shutil.get_terminal_size().columns
  half = int((width - 3)/2)
  if len(text) > width:
    text = re.sub(r'^(.{' + str(half) + '}).*(.{' + str(half) + '})$', '\g<1>...\g<2>', text)
  sys.stdout.write('{:{}.{}}'.format(text, 2*half + 3, 2*half + 3))

def printHeadline():
  print(\
'   _____       _     _ ______ _     _     \n'\
'  / ____|     | |   | |  ____(_)   | |    \n'\
' | |  __  ___ | | __| | |__   _ ___| |__  \n'\
' | | |_ |/ _ \| |/ _` |  __| | / __| \'_ \ \n'\
' | |__| | (_) | | (_| | |    | \__ \ | | |\n'\
'  \_____|\___/|_|\__,_|_|    |_|___/_| |_|\n'\
)



backupDirTo = '/backupDirTo'
backupDirFrom = ['/backupDirFrom']

prevBackups = list(reversed(os.listdir(backupDirTo)))

today = time.strftime('%Y%m%d_%H%M')
dirToday = os.path.join(backupDirTo, today)
os.mkdir(dirToday)

printHeadline()

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
      printToTerminalSize(os.path.join(relPath, file))
      sys.stdout.flush()
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
        sys.stdout.write('\r')
        sys.stdout.flush()
        printToTerminalSize(' ')
        sys.stdout.write('\r')
        sys.stdout.flush()
        print('    ' + os.path.join(relPath, file))
        shutil.copy2(fileFrom, fileTo)
        sizeCopied += os.stat(fileFrom).st_size
      else:
        sys.stdout.write('\r')
        sys.stdout.flush()
        printToTerminalSize(' ')
        sys.stdout.write('\r')
        sys.stdout.flush()

  print('  Copied: ' + readableSize(sizeCopied))
  print('  Linked: ' + readableSize(sizeLinked))

