#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import traceback


def main():
    parser = argparse.ArgumentParser(description='Booyakasha!')
    parser.add_argument('-F', '--foo', required=True, help='foo')
    parser.add_argument('-B', '--bar', help='bar')
    args = parser.parse_args()

    print args.foo,
    if args.bar:
        print args.bar

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except KeyboardInterrupt, e:
        raise e
    except SystemExit, e:
        raise e
    except Exception, e:
        print str(e)
        traceback.print_exc()
        sys.exit(1)
