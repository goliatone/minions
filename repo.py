#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import traceback
import glob
import yaml
from subprocess import call
"""
Can we read this?! That is a good question!
"""


class TemplateRepo():
    INIT_FILE = "__init__.*"

    def __init__(self):
        self.metadata = {}

    def list(self, path='~/.cookiejar'):
        path = os.path.expanduser(path)
        print path
        dirs = self.list_dirs(path)
        for dir in dirs:
            if os.path.isdir(dir):
                self.get_template_info(dir)
        self.print_metadata()

    def print_metadata(self):
        print "Templates:\n"
        for name in self.metadata:
            info = self.metadata[name]
            info.setdefault('Description', 'This template has no description')
            print "\t\t - {Template}\n\t\t {Description}".format(**info)

    def get_template_info(self, path):
        init_file = os.path.join(path, TemplateRepo.INIT_FILE)
        template = os.path.basename(path)
        content = init_file
        file = glob.glob(init_file)
        if file:
            content = open(file[0], 'r').readlines()
            b = [i for i in range(len(content)) if content[i] == '"""\n']
            if b.__len__() != 2:
                return
            content = "".join(content[b[0]+1:b[1]])
            self.metadata[template] = yaml.load(content)

    def list_dirs(self, path):
        output = []
        for item in os.listdir(path):
            dir = os.path.join(path, item)
            if os.path.isdir(dir):
                output.append(dir)
        return output

    def install(self, src='zip', dest='~/.cookiejar'):
        call(["cp", "-R", src, dest])


def main():
    parser = argparse.ArgumentParser(description='Booyakasha!')
    #first optional argument:
    parser.add_argument('-F', '--foo', required=False, help='foo')
    parser.add_argument('-B', '--bar', help='bar')
    args = parser.parse_args()

    repo = TemplateRepo()
    # repo.list()
    # repo.install()


if __name__ == '__main__':
    try:
        from scaffolder.main import CommandController
        manager = CommandController(sys.argv)
        manager.execute()
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
