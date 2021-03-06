#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse
import traceback
import glob
import yaml
import tempfile
from scaffolder.vcs import VCS
from textwrap import fill
from clint.textui import puts, indent, colored
from scaffolder.core.utils import clone_url, extract_directory, lower_keys, cp_recursive
from scaffolder import get_minion_path
from scaffolder.core.utils import Utils
"""
TemplateManager class:
Methods:
- list
- info <NAME>
- update <NAME>
- delete <NAME>
- install <URL|PATH>
- open <NAME>
- hooks <NAME>

"""
class TemplateManager():
    INIT_FILE = "meta.*"

    def __init__(self):
        self.metadata = {}

    def list(self, path=get_minion_path('weaver')):
        path = os.path.expanduser(path)
        dirs = self.list_dirs(path)
        for dir in dirs:
            if os.path.isdir(dir):
                self.load_metadata(dir)
        self.dump_metadata()

    def dump_metadata(self):
        print "Templates:\n"
        for name in self.metadata:
            self.print_metadata(name)

    def print_metadata(self, name):
        try:
            info = self.metadata[name]
            info.setdefault('description', 'This template has no description')
            # " %-45s %-15s %15s" % (template, status, file_type)
            title = "- {template}:\n".format(**info)
            desc = "{description}".format(**info)
            desc = fill(desc, width=70, initial_indent="  ", subsequent_indent="  ")
            puts(colored.green(
                title+desc
            ))
        except:
            puts(colored.red(
                "No metadata available for {}".format(name)
            ))


    def load_metadata(self, path):
        init_file = os.path.join(path, TemplateManager.INIT_FILE)
        template = os.path.basename(path)
        file = glob.glob(init_file)[0]
        try:
            with open(file, 'r') as file:
                metadata = yaml.load(file.read())
                self.metadata[template] = lower_keys(metadata)
        except:
            pass

    def list_dirs(self, path):
        output = []
        for item in os.listdir(path):
            dir = os.path.join(path, item)
            if os.path.isdir(dir):
                output.append(dir)
        return output

    def install(self, src='zip', dest='~/.minions/weaver'):
        #Check if dest is empty, if not, promt?
        #check if src is valid file, or dest valid file.
        #most of the time, dest should be default.
        #check to see if src is zip, or if src is vcs.

        if not ".git" in src:
            src = Utils.normalize_path(src)
        dest = Utils.normalize_path(dest)

        #TODO: we should clone and extract to tmp directory
        # and then cp.
        src, dest = clone_url(src=src, tgt=dest)
        src, dest = extract_directory(src=src, tgt=dest)
        if not ".zip" and not ".git" in src:
            cp_recursive(src, dest)

def main():
    parser = argparse.ArgumentParser(description='Booyakasha!')
    #first optional argument:
    parser.add_argument('-F', '--foo', required=False, help='foo')
    parser.add_argument('-B', '--bar', help='bar')
    args = parser.parse_args()

    repo = TemplateManager()
    repo.list()
    # repo.install()


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
