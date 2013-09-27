#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/15583870/mixing-positional-and-optional-arguments-in-argparse
import sys
import argparse
import traceback
import zipfile
import json
import tempfile
import contextlib
import shutil
import os
from subprocess import call


class Context():
    def __init__(self, context_file=None):
        self.context_file = context_file
        self.load()

    def load(self):
        with open(self.context_file, 'r') as content_file:
            config = content_file.read()
            self.context = json.loads(config)
        print "Loaded:\n {0}".format(config)

    def set_var(self, key, value):
        self.context[key] = value

    def get_context(self):
        return self.context


class Template():
    def __init__(self, context):
        self.context = context

    def replace(self, path):
        dest = path.format(**self.context)
        pdest = os.path.dirname(dest)
        print "Dest: {}".format(pdest)
        if not os.path.isdir(pdest):
            os.makedirs(pdest)
        with open(path, 'r') as src, open(dest, 'w+') as new:
            out = src.read().format(**self.context)
            new.write(out)


class Bootstrapper():
    def config(self, template=None, context_file=None, output=None):
        print template
        print context_file
        self.src = template
        self.context = Context(context_file)
        self.template = Template(self.context.get_context())
        self.context.set_var('__src__', 'output')
        if not os.path.isdir(output):
            os.makedirs(output)
        self.out_dir = output

    def create(self):
        print "Creating bootstrap"
        with self.make_tmp_dir() as tmp:
            src = os.path.join(tmp, '{__src__}')
            out = os.path.join(tmp, 'output')
            os.makedirs(src)
            with zipfile.ZipFile(self.src, 'r') as zfile:
                zfile.extractall(src)
                tfiles = self.list_files(src)
                for f in tfiles:
                    self.template.replace(f)
                shutil.rmtree(src)
            call(["cp", "-R", out+'/', self.out_dir])

    def list_files(self, path):
        output = []
        for root, dirs, files in os.walk(path):
            print('{}/'.format(root))
            for f in files:
                output.append('{}/{}'.format(root, f))
                print('{}/{}'.format(root, f))
        return output

    def clean(self, paths, tmp):
        print "Cleaning up:"
        print tmp
        for p in paths:
            os.remove(p)
        print paths
        pass

    @contextlib.contextmanager
    def make_tmp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)


def main():
    parser = argparse.ArgumentParser(description='Booyakasha!')
    parser.add_argument('-t', '--template',
                        default='gtrap.zip', help='Template file.')
    parser.add_argument('-c', '--context-file',
                        dest="context_file",
                        required=True, help='Context file')
    parser.add_argument('-o', '--output',
                        dest="output", default='./output',
                        required=False, help='Output directory')
    args = parser.parse_args()

    boot = Bootstrapper()
    boot.config(template=args.template,
                output=args.output,
                context_file=args.context_file)
    boot.create()

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
