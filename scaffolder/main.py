#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from scaffolder.cli import CommandController



def main(argv=None):
    if argv is None:
        argv = sys.argv

    manager = CommandController(argv)
    manager.execute()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))