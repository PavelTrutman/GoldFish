#!/usr/bin/python3

import pathlib
import datetime
from .database import Database

def getBackups(config):
  """
  Returns list of the backups on the media and in the database.

  Args:
    config (Config): configuration object

  Ruturns:
    dict: list of backups
  """

  dirTo = pathlib.Path(config.backupDirTo)
  backups = list(dirTo.iterdir())
  backups.sort(reverse=True)
  
  backupsDict = {}

  # get backups from HDD
  for backup in backups:
    if backup.is_dir():
      backupItems = backup.iterdir()
      backupsDict[backup.name] = {}
      for item in backupItems:
        backupsDict[backup.name][item.name] = {'HDD': True, 'DB': False}

  # get backups form DB
  dbPath = pathlib.Path(config.dbPath)
  if config.dbEnable:
    for backup in backups:
      dbPathBackup = dbPath / (backup.name + '.sqlite')
      if dbPathBackup.is_file():
        db = Database(dbPathBackup, readonly=True)
        backupItems = db.getFolders()
        if backup.name not in backupsDict:
          backupsDict[backup] = {}
        for _, item in backupItems:
          if item not in backupsDict[backup.name]:
            backupsDict[backup.name][item] = {'HDD': False, 'DB': True}
          else:
            backupsDict[backup.name][item]['DB'] = True

  return backupsDict
