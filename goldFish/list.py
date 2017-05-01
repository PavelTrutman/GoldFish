#!/usr/bin/python3

import os
import pathlib
import datetime
import terminaltables
from .io import *
from .config import Config
from .database import Database

class List:

  def main(configFile):
    """
    List Backups on the media.

    Args:
      configFile (str): path to the configuration file
    """

    config = Config(configFile)

    # load database
    if config.dbEnable:
      db = Database(config.dbPath)

    dirToPath = pathlib.Path(config.backupDirTo)
    backups = os.listdir(str(dirToPath))
    backups.sort(reverse=True)
    
    printHeadline()

    backupsDict = {}

    # get backups from HDD
    for backup in backups:
      backupFolder = dirToPath.joinpath(backup)
      backupItems = os.listdir(str(backupFolder))
      backupDatetime = datetime.datetime.strptime(backup, '%Y%m%d_%H%M')
      backupDatetimeStr = backupDatetime.strftime('%Y-%m-%d %H:%M')
      backupsDict[backupDatetimeStr] = {}
      for item in backupItems:
        backupsDict[backupDatetimeStr][item] = {'HDD': True, 'DB': False}

    # get backups form DB
    if config.dbEnable:
      backups = db.getBackups()
      for backupId, backup in backups:
        backupItems = db.getFolders(backupId)
        backupDatetime = datetime.datetime.strptime(backup, '%Y%m%d_%H%M')
        backupDatetimeStr = backupDatetime.strftime('%Y-%m-%d %H:%M')
        if backupDatetimeStr not in backupsDict:
          backupsDict[backupDatetimeStr] = {}
        for _, item in backupItems:
          if item not in backupsDict[backupDatetimeStr]:
            backupsDict[backupDatetimeStr][item] = {'HDD': False, 'DB': True}
          else:
            backupsDict[backupDatetimeStr][item]['DB'] = True

    # create table
    tableData = [['Datetime', 'Folder', 'HDD', 'DB']]
    backups = list(backupsDict.keys())
    backups.sort(reverse=True)
    for backup in backups:
      items = list(backupsDict[backup].keys())
      items.sort()
      for item, i in zip(items, range(len(items))):
        if i == 0:
          tableData.append([backup, item, '', ''])
        else:
          tableData.append(['', item, '', ''])
        if backupsDict[backup][item]['HDD']:
          tableData[-1][2] = 'X'
        if backupsDict[backup][item]['DB']:
          tableData[-1][3] = 'X'

    table = terminaltables.SingleTable(tableData)
    table.justify_columns[2] = 'center'
    table.justify_columns[3] = 'center'
    print(table.table)

