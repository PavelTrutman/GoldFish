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

    if hasattr(self, 'connection'):
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


  def newBackup(self, name):
    """
    Inserts new backup into the database.

    Args:
      name (str): name of the backup

    Returns:
      int: id of the inserted backup
    """

    self.db.execute('INSERT INTO backups(name) VALUES(?)', (name, ))
    self.connection.commit()
    return self.db.lastrowid


  def newFolder(self, name, backupId):
    """
    Inserts new backup folder into the database.

    Args:
      name (str): name of the folder
      backupId (int): id of the current backup

    Returns:
      int: id of the inserted folder
    """

    self.db.execute('INSERT INTO folders(name, backupId) VALUES(?, ?)', (name, backupId))
    self.connection.commit()
    return self.db.lastrowid


  def getBackup(self, name):
    """
    Selects backup id based on backup name.

    Args:
      name (str): name of the backup

    Returns:
      int: id of the backup
    """

    self.db.execute('SELECT id FROM backups WHERE name = ? LIMIT 1', (name, ))
    res = self.db.fetchone()
    self.connection.commit()
    if res == None:
      return None
    else:
      return res[0]


  def getFolder(self, name, backupId):
    """
    Selects folder id based on folder name and backup id.

    Args:
      name (str): name of the folder
      backupId (int): id of the backup

    Returns:
      int: id of the folder
    """

    if backupId == None:
      return None

    self.db.execute('SELECT id FROM folders WHERE name = ? AND backupId = ? LIMIT 1', (name, backupId))
    res = self.db.fetchone()
    self.connection.commit()
    if res == None:
      return None
    else:
      return res[0]


  def getFile(self, path, folderId):
    """
    Selects file id based on the path of the file and folder id.

    Args:
      path (str): path to the file
      folderId (int): id of the folder

    Returns:
      int: id of the file
    """

    if folderId == None:
      return None, None

    self.db.execute('SELECT id, hashId FROM files WHERE path = ? AND folderId = ? LIMIT 1', (path, folderId))
    res = self.db.fetchone()
    self.connection.commit()
    if res == None:
      return None, None
    else:
      return res


  def insertFile(self, path, folderId, hashId):
    """
    Inserts new file into the databse.

    Args:
      path (str): path to the file
      folderId (int): id of the folder
      hashId (int): id of the hash

    Returns:
      int: id of the inserted file
    """

    self.db.execute('INSERT INTO files(path, folderId, hashId)  VALUES (?, ?, ?)', (path, folderId, hashId))
    self.connection.commit()
    return self.db.lastrowid


  def getHashId(self, hash, size):
    """
    Select hash id based on the hash and file size.

    Args:
      hash (str): hash of the file
      size (int): size of the file in bytes

    Returns:
      int: id of the hash
    """

    self.db.execute('SELECT id FROM hashes WHERE hash = ? AND size = ? LIMIT 1', (hash, size))
    res = self.db.fetchone()
    self.connection.commit()
    if res == None:
      return None
    else:
      return res[0]


  def insertHash(self, hash, size):
    """
    Inserts new hash into the databse.

    Args:
      hash (str): hash of the file
      size (int): size of the file

    Returns:
      int: id of the inserted hash
    """

    self.db.execute('INSERT INTO hashes(hash, size)  VALUES (?, ?)', (hash, size))
    self.connection.commit()
    return self.db.lastrowid


  def getFilesByHash(self, hashId):
    """
    Obtains list of files with the same hash.

    Args:
      hashId (int): id of the hash

    Returns:
      list: list of files with the same hash
    """

    self.db.execute('SELECT files.id, backups.name, folders.name, files.path FROM files, folders, backups WHERE files.hashId = ? AND files.folderId = folders.id AND folders.backupId = backups.id ORDER BY files.id DESC', (hashId, ))
    res = self.db.fetchall()
    self.connection.commit()
    return res


class DatabaseError(Exception):
  """
  Exception for handling database errors.
  """


  pass 
