#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from scaffolder.core.commands import  CommandController



def run(argv=None):
    if argv is None:
        argv = sys.argv

    manager = CommandController()
    manager.execute(argv)
    return 0

if __name__ == '__main__':
    sys.exit(
        run(sys.argv)
    )
