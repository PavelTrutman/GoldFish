#!/usr/bin/python3

import os
import shutil
import time
import math
import sys
import re
import hashlib
import argparse
from .io import *
from .config import Config
from .database import Database


def main():

  # command line arguments parser
  parser = argparse.ArgumentParser(add_help=False)
  parser.prog = 'goldFish';
  
  parser.add_argument('--help', '-h', action='help', help='show this help message and exit')
  parser.add_argument('configFile', type=str, help='path to the config file')
  args = parser.parse_args()


  config = Config(args.configFile)

  # load database
  if config.dbEnable:
    db = Database(config.dbPath)

  prevBackups = os.listdir(config.backupDirTo)
  prevBackups.sort(reverse=True)
  
  today = time.strftime('%Y%m%d_%H%M')
  dirToday = os.path.join(config.backupDirTo, today)
  os.mkdir(dirToday)

  printHeadline()

  if config.dbEnable:
    print('Using database.')
    backupId = db.newBackup(today)

  print('Creating new backup: ' + today)
  
  for dirFrom in config.backupDirFrom:
    backupDir = os.path.basename(dirFrom)
    dirTo = os.path.join(dirToday, backupDir)
    os.mkdir(dirTo)
    if config.dbEnable:
      folderId = db.newFolder(backupDir, backupId)
  
    # find prev backup
    dirPrev = None
    datePrev = None
    backupIdPrev = None
    folderIdPrev = None
    for prev in prevBackups:
      dirPrevTmp = os.path.join(config.backupDirTo, prev, backupDir)
      if os.path.isdir(dirPrevTmp):
        dirPrev = dirPrevTmp
        datePrev = prev
        if config.dbEnable:
          backupIdPrev = db.getBackup(datePrev)
          folderIdPrev = db.getFolder(backupDir, backupIdPrev)
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
    sizeHashLinked = 0
   
    for root, dirs, files in os.walk(dirFrom):
      relPath = os.path.relpath(root, dirFrom)
      if relPath == '.':
        relPath = ''
      curDirTo = os.path.join(dirTo, relPath)
      for dir in dirs:
        os.mkdir(os.path.join(curDirTo, dir))
      for file in files:
        fileFrom = os.path.join(root, file)
        fileTo = os.path.join(curDirTo, file)
        printToTerminalSize('  ' + os.path.join(relPath, file))
        sys.stdout.flush()
        sys.stdout.write('\r')
        sys.stdout.flush()
        copied = False
        statFrom = os.stat(fileFrom)
        if not (dirPrev is None):
          filePrev = os.path.join(dirPrev, relPath, file)
          if os.path.isfile(filePrev):
            statPrev = os.stat(filePrev)
            if (statFrom.st_size == statPrev.st_size) and (round(statFrom.st_mtime) == round(statPrev.st_mtime)):

              # link from previous backup
              os.link(filePrev, fileTo)
              copied = True
              sizeLinked += statFrom.st_size

              if config.dbEnable:
                # update db
                fileIdPrev, hashIdPrev = db.getFile(os.path.join(relPath, file), folderIdPrev)
                if fileIdPrev == None:

                  # compute hash
                  sys.stdout.write('H')
                  sys.stdout.flush()
                  sys.stdout.write('\r')
                  sys.stdout.flush()
                  fileHash = hashFile(fileFrom)
                  fileSize = statFrom.st_size
                  hashId = db.getHashId(fileHash, fileSize)
                  if hashId == None:
                    hashId = db.insertHash(fileHash, fileSize)
                  db.insertFile(os.path.join(relPath, file), folderId, hashId)
                  
                else:

                  # insert new file into the db using prev file
                  db.insertFile(os.path.join(relPath, file), folderId, hashIdPrev)
              
        if not copied:

          linked = False
          mtimeDiffer = False
          if config.dbEnable:
            # compute hash
            sys.stdout.write('H')
            sys.stdout.flush()
            sys.stdout.write('\r')
            sys.stdout.flush()
            fileHash = hashFile(fileFrom)
            fileSize = statFrom.st_size
            hashId = db.getHashId(fileHash, fileSize)
            if hashId == None:
              hashId = db.insertHash(fileHash, fileSize)
            else:

              # find file with same hash
              sameFiles = db.getFilesByHash(hashId)
              for sFile in sameFiles:
                sFilePath = os.path.join(config.backupDirTo, sFile[1], sFile[2], sFile[3])
                if os.path.isfile(sFilePath):
                  sFileStat = os.stat(sFilePath)
                  fromStat = os.stat(fileFrom)
                  if round(sFileStat.st_mtime) == round(fromStat.st_mtime):
                    os.link(sFilePath, fileTo)
                    linked = True
                    sizeHashLinked += statFrom.st_size
                    break
              if not linked:
                for sFile in sameFiles:
                  sFilePath = os.path.join(config.backupDirTo, sFile[1], sFile[2], sFile[3])
                  if os.path.isfile(sFilePath):
                    mtimeDiffer = True
                    if config.dbLinkMDiffer:
                      os.link(sFilePath, fileTo)
                      if os.stat(fileFrom).st_mtime > os.stat(sFilePath).st_mtime:
                        shutil.copystat(fileFrom, fileTo)
                      linked = True
                      sizeHashLinked += statFrom.st_size
                    break
                
            db.insertFile(os.path.join(relPath, file), folderId, hashId)
          

          if not linked:
            sys.stdout.write('C')
            sys.stdout.flush()
            sys.stdout.write('\r')
            sys.stdout.flush()
            shutil.copy2(fileFrom, fileTo)
            sizeCopied += statFrom.st_size
          printToTerminalSize(' ')
          sys.stdout.write('\r')
          sys.stdout.flush()
          print('    ' + os.path.join(relPath, file))
          if linked:
            if mtimeDiffer:
              print('      hash linked with different mtime with ' + os.path.join(sFile[1], sFile[2], sFile[3]))
            else:
              print('      hash linked with ' + os.path.join(sFile[1], sFile[2], sFile[3]))
          else:
            if mtimeDiffer:
              print('      may be hash linked with different mtime with ' + os.path.join(sFile[1], sFile[2], sFile[3]))
            
        else:
          printToTerminalSize(' ')
          sys.stdout.write('\r')
          sys.stdout.flush()

    os.sync()

    print('  Copied:     ' + readableSize(sizeCopied))
    print('  Linked:     ' + readableSize(sizeLinked))
    print('  HashLinked: ' + readableSize(sizeHashLinked))

if __name__ == "__main__":
  main()
