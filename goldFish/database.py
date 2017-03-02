#!/usr/bin/python3

import sqlite3
import pathlib
from .io import *

class Database:
  """
  Class maintaining the database.

  by Pavel Trutman, pavel.trutman@fel.cvut.cz
  """


  def __init__(self, path):
    """
    Connects to the database.

    Args:
      path (str): path to the sqlite database file

    Returns:
      None
    """

    create = False
    self.path = pathlib.Path(path)
    if not self.path.exists():
      if queryYesNo('The database at ' + str(self.path) + ' does not exists. Do you want to create it?', default='yes'):
        create = True
      else:
        raise DatabaseError('Database at ' + str(self.path) + ' does not exists and will not be created.')

    self.connection = sqlite3.connect(str(self.path))
    self.db = self.connection.cursor()
    self.db.execute('PRAGMA foreign_keys = ON')

    if create:
      self.create()


  def __del__(self):
    """
    Destroys the object.

    Args:

    Returns:
      None
    """

    self.connection.commit()
    self.connection.close()


  def create(self):
    """
    Initialize new database and creates required tables.

    Args:

    Returns:
      None
    """

    self.db.execute('CREATE TABLE backups(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE)')
    self.db.execute('CREATE TABLE folders(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, backupId INTEGER REFERENCES backups(id) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT folders_unique__name_backupId UNIQUE(name, backupId))')
    self.db.execute('CREATE TABLE hashes(id INTEGER PRIMARY KEY AUTOINCREMENT, hash TEXT, size INTEGER, CONSTRAINT hashes_unique__hash_size UNIQUE(hash, size))')
    self.db.execute('CREATE TABLE files(id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, folderId INTEGER REFERENCES folders(id) ON DELETE CASCADE ON UPDATE CASCADE, hashId INTEGER REFERENCES hashes(id) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT files_unique__path_folderId UNIQUE(path, folderId))')
    self.connection.commit()


class DatabaseError(Exception):
  """
  Exception for handling database errors.
  """


  pass 
