#!/usr/bin/python3

import terminaltables
from .io import *
from .config import Config
from .backups import *
from .database import Database

class List:

  def main(configFile):
    """
    List Backups on the media.

    Args:
      configFile (str): path to the configuration file

    Returns:
      None
    """

    config = Config(configFile)

    printHeadline()

    backupsDict = getBackups(config)
    printBackups(backupsDict)
