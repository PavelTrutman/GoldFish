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
@click.option('--dry-run', is_flag=True)
@common_params
def backup(config, dry_run):

  from .backup import Backup

  Backup.main(config, dry_run)


@cli.command(short_help='List all backups.', help='Lists all backups on the drive and in the database.')
@common_params
def list(config):

  from .list import List

  List.main(config)


@cli.command(short_help='Prune needless backups.', help='Prune backups that are needless.')
@common_params
def prune(config):

  from .prune import Prune

  Prune.main(config)


@cli.command(short_help='Get size of folder in the backup.', help='Get size of folder in the backup.')
@click.argument('path', type=click.Path(exists=True, readable=True))
@click.help_option('--help', '-h')
def size(path):

  from .size import Size

  Size.main(path)


if __name__ == '__main__':
  cli()
