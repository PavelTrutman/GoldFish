#!/usr/bin/python3

import os
import pathlib
import datetime

def getBackups(config, db):
  """
  Returns list of the backups on the media and in the database.

  Args:
    config (Config): configuration object
    db (Database): database object

  Ruturns:
    dict: list of backups
  """

  dirToPath = pathlib.Path(config.backupDirTo)
  backups = os.listdir(str(dirToPath))
  backups.sort(reverse=True)
  
  backupsDict = {}

  # get backups from HDD
  for backup in backups:
    backupFolder = dirToPath.joinpath(backup)
    if backupFolder.is_dir():
      backupItems = os.listdir(str(backupFolder))
      backupsDict[backup] = {}
      for item in backupItems:
        backupsDict[backup][item] = {'HDD': True, 'DB': False}

  # get backups form DB
  if config.dbEnable:
    backups = db.getBackups()
    for backupId, backup in backups:
      backupItems = db.getFolders(backupId)
      if backup not in backupsDict:
        backupsDict[backup] = {}
      for _, item in backupItems:
        if item not in backupsDict[backup]:
          backupsDict[backup][item] = {'HDD': False, 'DB': True}
        else:
          backupsDict[backup][item]['DB'] = True

  return backupsDict
