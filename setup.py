#!/usr/bin/python3

from setuptools import setup

"""
Setup script for backup module distribution.

by Pavel Trutman, pavel.tutman@fel.cvut.cz
"""

setup (
  # Distribution meta-data
  name='goldFish',
  version='0.1',
  description='Backup utility for incremental backups.',
  long_description='GoldFish is a backup utility for creating incremental backups. When creating new backup a hardlink is created if the same file exists in previous backup, if not the file is copied to the backup.',
  author='Pavel Trutman',
  author_email='pavel.trutman@fel.cvut.cz',
  url='https://github.com/PavelTrutman/GoldFish',
  package_dir={'GoldFish' : '.'},
  packages = ['goldFish'],
  install_requires = [
    'pyyaml',
    'click',
    'terminaltables',
  ],
  entry_points={'console_scripts': ['goldFish = goldFish.cli:cli']},
)
