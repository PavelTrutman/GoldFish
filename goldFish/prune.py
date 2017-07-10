#!/usr/bin/python3

import terminaltables
from .io import *
from .config import Config
from .backups import *
from .database import Database

class Prune:

  def main(configFile):
    """
    Prune backups that are needless.

    Args:
      configFile (str): path to the configuration file
    """

    config = Config(configFile)

    # load database
    if config.dbEnable:
      db = Database(config.dbPath)
    else:
      db = None

    printHeadline()

    backupsDict = getBackups(config, db)
    printBackups(backupsDict)

    if db:
      backups = list(backupsDict.keys())
      backups.sort(reverse=True)
      for backup in backups:
        items = list(backupsDict[backup].keys())
        items.sort()
        backupId = db.getBackup(backup)
        for item in items:
          if not backupsDict[backup][item]['HDD'] and backupsDict[backup][item]['DB']:
            if queryYesNo('Backup {backup} {item} is stored in the database, but not stored physicaly on the drive. Do you want to remove it from the database?'.format(backup=backup, item=item), default='no'):
              folderId = db.getFolder(item, backupId)
              print('Removing ...', end='', flush=True)
              db.removeFolder(backupId, folderId)
              print(' Done')
