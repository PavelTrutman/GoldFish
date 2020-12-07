#!/usr/bin/python3

import pathlib
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

    printHeadline()

    backupsDict = getBackups(config)
    printBackups(backupsDict)

    if config.dbEnable:
      backups = list(backupsDict.keys())
      backups.sort(reverse=True)
      for backup in backups:
        items = list(backupsDict[backup].keys())
        items.sort()
        #backupId = db.getBackup(backup)
        for item in items:
          if not backupsDict[backup][item]['HDD'] and backupsDict[backup][item]['DB']:
            if queryYesNo('Backup {backup} {item} is stored in the database, but not stored physicaly on the drive. Do you want to remove it from the database?'.format(backup=backup, item=item), default='no'):
              db = Database(pathlib.Path(config.dbPath) / (backup + '.sqlite'))
              folderId = db.getFolder(item)
              print('Removing ...', end='', flush=True)
              db.removeFolder(folderId)
              print(' Done')
