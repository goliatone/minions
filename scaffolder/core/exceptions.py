#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. module:: scaffolder.core.exceptions
   :synopsis: Custom Minion exception classes
"""

import sys

from clint.textui import indent, puts
from clint.textui.colored import red


class MinionException(Exception):
    """
    Base exception class. All Minion-specific exceptions should subclass
    this class.
    """
    def __init__(self, message):
        with indent(4, quote=' >'):
            puts(red('Error: {0}'.format(message)))
            puts(red('Exiting'))
        sys.exit()

class NonTemplatedInputDirException(MinionException):
    """
    Raised when a project's input dir is not templated.
    The name of the input directory should always contain a string that is
    rendered to something else, so that input_dir != output_dir.
    """

class UnknownDirectoryException(MinionException):
    """
    Raised when feeded an unknow
    """

class MissingArgument(MinionException):
    """
    Raised when Bootstrapper cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """

class UnknownTemplateDirException(MinionException):
    """
    Raised when Bootstrapper cannot determine which directory is the project
    template, e.g. more than one dir appears to be a template dir.
    """

class MissingProjectDir(MinionException):
    """
    Raised during cleanup when remove_repo() can't find a generated project
    directory inside of a repo.
    """

class ConfigDoesNotExistException(MinionException):
    """
    Raised when get_config() is passed a path to a config file, but no file
    is found at that path.
    """

class InvalidConfiguration(MinionException):
    """
    Raised if the global configuration file is not valid YAML or is
    badly contructed.
    """

class UnknownRepoType(MinionException):
    """
    Raised if a repo's type cannot be determined.
    """