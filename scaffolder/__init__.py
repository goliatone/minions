# -*- coding: utf-8 -*-
import os

VERSION = (0, 0, 1, 'dev')

MINIONS_PATH = '~/.minions'

__version__ = '.'.join((str(each) for each in VERSION[:4]))

__author__ = 'goliatone'


def get_version():
    return '.'.join((str(each) for each in VERSION[:3]))

def get_minion_path(minion=None):
    if not minion:
        return os.path.expanduser(MINIONS_PATH)
    return os.path.join(get_minion_path(), minion)

#TODO: This will break, need to use setup tools.
def install_minion_config(minion=None):
    if not os.path.isdir(get_minion_path()):
        os.mkdir(get_minion_path())

    if not os.path.isdir(get_minion_path(minion)):
        os.mkdir(get_minion_path(minion))

    filename = "%src" % minion
    template = "%s.template" % filename
    output   = ".%s" % filename
    if not os.path.isfile(get_minion_path(output)):
       pass