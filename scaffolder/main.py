#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from scaffolder.cli import CommandController



def main(argv=None):
    if argv is None:
        argv = sys.argv

    manager = CommandController()
    manager.execute(argv)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))