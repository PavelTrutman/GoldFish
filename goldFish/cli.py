#!/usr/bin/python3

import click
import functools

def common_params(func):
  @click.argument('config', type=click.Path(exists=True, readable=True))
  @click.help_option('--help', '-h')
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return wrapper


@click.group()
@click.help_option('--help', '-h')
def cli():
  pass


@cli.command(short_help='Create new backup.', help='Creates new backup as defined in the CONFIG file.')
@common_params
def backup(config):

  from .backup import Backup

  Backup.main(config)


#@cli.command()
#@common_params
#def backupSize(configFile):
  #print('Backup size')


if __name__ == '__main__':
  cli()
