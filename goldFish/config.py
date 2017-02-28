#!/usr/bin/python3

import os
import yaml

class Config:
  """
  Class responsible for configuration file loading and for providing default values of missing items.

  by Pavel Trutman, pavel.trutman@fel.cvut.cz
  """


  """
  Default config.
  """
  defaultConfig = {
    'backupDirTo': '',
    'backupDirFrom': [],
  }


  def __init__(self, path):
    """
    Initialization of the object.

    Args:
      path (str): path to the config file

    Returns:
      None
    """

    self.update(path)


  def load(self, fileName):
    """
    Loads config from the given path.

    Args:
      path (str): path to the config file

    Returns:
      dict: loaded config
    """

    with open(fileName, 'r') as ymlfile:
      cfg = yaml.safe_load(ymlfile)
    if not isinstance(cfg, dict):
      raise ConfigFileError('Configuration file does not parse as a dictionary.')

    # merge loaded config with default values
    config = self.defaultConfig.copy()
    config.update(cfg)
    return config


  def update(self, path):
    """
    Updates the config object with the loaded config.

    Args:
      path (str): path to the config file

    Returns:
      None

    Throws:
      ConfigError: when some constraint violation occurs
      FileNotFoundError: when some of the backup folders does not exist
    """

    # laod config from file
    config = self.load(path)

    # check backuoDirTo
    if config['backupDirTo'] != '':
      if os.path.exists(config['backupDirTo']):
        self.backupDirTo = config['backupDirTo']
      else:
         raise FileNotFoundError(config['backupDirTo'])
    else:
      raise ConfigError('backupDirTo', config['backupDirTo'])

    if isinstance(config['backupDirFrom'], list) and len(config['backupDirFrom']) > 0:
      for p in config['backupDirFrom']:
        if not os.path.exists(p):
         raise FileNotFoundError(p)
      self.backupDirFrom = config['backupDirFrom']
    else:
      raise ConfigError('backupDirFrom', config['backupDirFrom'])

    # if everything pass, then save config
    self.config = config


class ConfigError(Exception):
  """
  Class for configuration exceptions.

  by Pavel Trutman, pavel.tutman@fel.cvut.cz
  """

  def __init__(self, attribute, value):
    """
    Overriding constructor.

    Args:
      attribute(str): Name of bad attribute.
      value (str): Bad value for the attribute.

    Returns:
      None
    """

    # calling super contructor
    super(Exception, self).__init__('Bad value \'{}\' given for attribute \'{}\'.'.format(str(value), attribute))


class ConfigFileError(Exception):
  """
  Class for configuration files exceptions.

  by Pavel Trutman, pavel.tutman@fel.cvut.cz
  """

  def __init__(self, message):
    """
    Overriding constructor.

    Args:
      message(str): Explanation of the exception.

    Returns:
      None
    """

    # calling super contructor
    super(Exception, self).__init__(message)
