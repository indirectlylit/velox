"""
Performance testing bootstrap script.

It will try to delete the current Kolibri related SQLite3
database files and copy the prepared db.sqlite3 file to be
used for tests.

Usage: python bootstrap.py; or:
       python bootstrap.py --kolibri-home=/path/to/kolibri/home/dir; or:
       KOLIBRI_HOME=/path/to/kolibri/home/dir python bootstrap.py
"""

import argparse
import errno
import os
import shutil


def bootstrap(args):
    """
    Start the bootstrap process:
      - set the KOLIBRI_HOME environment variable
      - delete the current Kolibri SQLite database
      - copy the database we previously prepared for testing
    """
    set_KOLIBRI_HOME(args.kolibri_home)

    delete_current_db()
    if copy_clean_db():
        pass


def copy_clean_db():
    """
    Copy the previously prepared testing database to the KOLIBRI_HOME directory
    """
    KOLIBRI_HOME = get_KOLIBRI_HOME()
    db_name = 'db.sqlite3'

    shutil.copyfile(os.path.join('data', db_name),
                    os.path.join(KOLIBRI_HOME, db_name))
    return os.path.exists(os.path.join(KOLIBRI_HOME, 'db.sqlite3'))


def delete_current_db():
    """
    Delete the current Kolibri SQLite databases
    """
    db_files = ['db.sqlite3', 'db.sqlite3-shm', 'db.sqlite3-wal']
    for db_file in db_files:
        try:
            os.remove(os.path.join(get_KOLIBRI_HOME(), db_file))
        except OSError as e:
            if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
                raise  # re-raise exception if a different error occurred


def set_KOLIBRI_HOME(kolibri_home_arg):
    """
    Set the KOLIBRI_HOME environment variable:
      - if the directory value has been passed as a script argument, use that
      - set the default value to be the one defined as per the Kolibri code
    """
    if kolibri_home_arg:
        KOLIBRI_HOME = kolibri_home_arg
    else:
        KOLIBRI_HOME = os.path.join(os.path.expanduser('~'), '.kolibri')

    os.environ.setdefault('KOLIBRI_HOME', KOLIBRI_HOME)


def get_KOLIBRI_HOME():
    """
    Return KOLIBRI_HOME environment variable
    """
    return os.environ.get('KOLIBRI_HOME')


if __name__ == '__main__':
    # read command line args
    parser = argparse.ArgumentParser(description='Velox bootstrap script.')
    parser.add_argument('--kolibri-home', dest='kolibri_home', help='path to the Kolibri installation')
    args = parser.parse_args()

    # start the bootstrap process
    bootstrap(args)
