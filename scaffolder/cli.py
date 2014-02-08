#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from scaffolder.core.commands import  CommandController


COMMANDS = [
    'create',
    'list',
    'install',
    'vcs',
]


class CliApplication():
    def __init__(self):
        self.description
    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

def run(argv=None):
    if argv is None:
        argv = sys.argv

    #Example of how we can access Meta class for each CMD
    from scaffolder.commands.vcs import VcsCommand
    meta = getattr(VcsCommand, 'Meta', None)

    manager = CommandController()
    #make command ids available
    manager.register_command_names(COMMANDS)
    manager.execute(argv)
    return 0

if __name__ == '__main__':
    sys.exit(
        run(sys.argv)
    )
