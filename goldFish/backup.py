#!/usr/bin/python3

import os
import shutil
import time
import math
import sys
import re
import hashlib
from .io import *
from .config import Config
from .database import Database

class Backup:

  def main(configFile, dryRun):
    """
    Creates new backup.

    Args:
      configFile (str): path to the configuration file
      dryRun (bool): whether in testing mode
    """

    config = Config(configFile)
    config.dryRun = dryRun

    # load database
    if config.dbEnable:
      if not config.dryRun:
        db = Database(config.dbPath)
      else:
        if pathlib.Path(config.dbPath).exists():
          db = Database(config.dbPath, readonly=True)
          db = db.moveToMemory()
        else:
          db = Database(Database.MEMORY)

    prevBackups = os.listdir(config.backupDirTo)
    prevBackups.sort(reverse=True)
    
    today = time.strftime('%Y%m%d_%H%M')
    dirToday = os.path.join(config.backupDirTo, today)
    if not config.dryRun:
      os.mkdir(dirToday)

    printHeadline()

    if config.dbEnable:
      print('Using database.')
      backupId = db.newBackup(today)

    print('Creating new backup: ' + today)
    
    for dirFrom in config.backupDirFrom:
      backupDir = os.path.basename(dirFrom)
      dirTo = os.path.join(dirToday, backupDir)
      if not config.dryRun:
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
      numFiles = 0
     
      for root, dirs, files in os.walk(dirFrom):
        relPath = os.path.relpath(root, dirFrom)
        if relPath == '.':
          relPath = ''
        curDirTo = os.path.join(dirTo, relPath)
        for dir in dirs:
          if not config.dryRun:
            os.mkdir(os.path.join(curDirTo, dir))
        for file in files:
          fileFrom = os.path.join(root, file)
          fileTo = os.path.join(curDirTo, file)
          printToTerminalSize('  ' + os.path.join(relPath, file))
          sys.stdout.flush()
          sys.stdout.write('\r')
          sys.stdout.flush()
          copied = False
          statFrom = os.stat(fileFrom, follow_symlinks=config.followSymlinks)
          if not (dirPrev is None):
            filePrev = os.path.join(dirPrev, relPath, file)
            if os.path.isfile(filePrev) or os.path.islink(filePrev):
              statPrev = os.stat(filePrev, follow_symlinks=config.followSymlinks)
              if (statFrom.st_size == statPrev.st_size) and (round(statFrom.st_mtime) == round(statPrev.st_mtime)):

                # link from previous backup
                if not config.dryRun:
                  os.link(filePrev, fileTo, follow_symlinks=config.followSymlinks)
                copied = True
                sizeLinked += statFrom.st_size
                numFiles += 1

                if config.dbEnable:
                  # update db
                  fileIdPrev, hashIdPrev = db.getFile(os.path.join(relPath, file), folderIdPrev)
                  if fileIdPrev == None:

                    # compute hash
                    sys.stdout.write('H')
                    sys.stdout.flush()
                    sys.stdout.write('\r')
                    sys.stdout.flush()
                    fileHash, fileSymlink = hashFile(fileFrom, config.followSymlinks)
                    fileSize = statFrom.st_size
                    hashId = db.getHashId(fileHash, fileSize, fileSymlink)
                    if hashId == None:
                      hashId = db.insertHash(fileHash, fileSize, fileSymlink)
                    db.insertFile(os.path.join(relPath, file), round(statFrom.st_mtime), folderId, hashId)
                    
                  else:

                    # insert new file into the db using prev file
                    db.insertFile(os.path.join(relPath, file), round(statFrom.st_mtime), folderId, hashIdPrev)
                
          if not copied:

            linked = False
            mtimeDiffer = False
            if config.dbEnable:
              # compute hash
              sys.stdout.write('H')
              sys.stdout.flush()
              sys.stdout.write('\r')
              sys.stdout.flush()
              fileHash, fileSymlink = hashFile(fileFrom, config.followSymlinks)
              fileSize = statFrom.st_size
              hashId = db.getHashId(fileHash, fileSize, fileSymlink)
              if hashId == None:
                hashId = db.insertHash(fileHash, fileSize, fileSymlink)
              else:

                # find file with same hash
                sameFiles = db.getFilesByHash(hashId)
                for sFile in sameFiles:
                  if round(statFrom.st_mtime) == sFile[4]:
                    sFilePath = os.path.join(config.backupDirTo, sFile[1], sFile[2], sFile[3])
                    if os.path.isfile(sFilePath) or (config.dryRun and sFile[1] == today):
                      if not config.dryRun:
                        os.link(sFilePath, fileTo, follow_symlinks=config.followSymlinks)
                      linked = True
                      sizeHashLinked += statFrom.st_size
                      numFiles += 1
                      break
                if not linked:
                  for sFile in sameFiles:
                    sFilePath = os.path.join(config.backupDirTo, sFile[1], sFile[2], sFile[3])
                    if os.path.isfile(sFilePath) or (config.dryRun and sFile[1] == today):
                      mtimeDiffer = True
                      if config.dbLinkMDiffer:
                        if not config.dryRun:
                          os.link(sFilePath, fileTo, follow_symlinks=config.followSymlinks)
                          if round(statFrom.st_mtime) > sFile[4]:
                            shutil.copystat(fileFrom, fileTo, follow_symlinks=config.followSymlinks)
                        linked = True
                        sizeHashLinked += statFrom.st_size
                        numFiles += 1
                        break
                  
              db.insertFile(os.path.join(relPath, file), round(statFrom.st_mtime), folderId, hashId)
            

            if not linked:
              sys.stdout.write('C')
              sys.stdout.flush()
              sys.stdout.write('\r')
              sys.stdout.flush()
              if not config.dryRun:
                shutil.copy2(fileFrom, fileTo, follow_symlinks=config.followSymlinks)
              sizeCopied += statFrom.st_size
              numFiles += 1
            printToTerminalSize(' ')
            sys.stdout.write('\r')
            sys.stdout.flush()
            print('    ' + os.path.join(relPath, file))
            if linked:
              if mtimeDiffer:
                print('      hash-linked with different mtime with ' + os.path.join(sFile[1], sFile[2], sFile[3]))
              else:
                print('      hash-linked with ' + os.path.join(sFile[1], sFile[2], sFile[3]))
            else:
              if mtimeDiffer:
                print('      may be hash-linked with different mtime with ' + os.path.join(sFile[1], sFile[2], sFile[3]))
              
          else:
            printToTerminalSize(' ')
            sys.stdout.write('\r')
            sys.stdout.flush()

      os.sync()

      print('  Copied:        ' + readableSize(sizeCopied))
      print('  Linked:        ' + readableSize(sizeLinked))
      print('  Hash-linked:   ' + readableSize(sizeHashLinked))
      print('  Files written: ' + str(numFiles))
