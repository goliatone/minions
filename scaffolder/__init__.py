# -*- coding: utf-8 -*-

VERSION = (0, 0, 1, 'dev')

__version__ = '.'.join((str(each) for each in VERSION[:4]))

__author__ = 'goliatone'


def get_version():
    return '.'.join((str(each) for each in VERSION[:3]))
