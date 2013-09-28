#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/15583870/mixing-positional-and-optional-arguments-in-argparse
import sys
from sys import platform
import argparse
import traceback
# import zipfile
import json
import tempfile
import contextlib
import shutil
import os
from subprocess import call, Popen, PIPE
import re
import ConfigParser

"""
TODO: Integrate into MinionTasks
A) Given a src template dir and a context file,
   interpolate and put in out dir.
B) Have global context, i.e username email github
C) Have templates dir @ ~/.cookiejars
D) Add new templates:
   - We clone from github // bitbucket?
   - We move from local dir.
E) Add on_created_hook.py in template src dir
F) Take -C "bower install && npm install" post cmd
G) Add exclude files.
"""


class Config():
    def __init__(self, path='~/.tmplater'):
        self.path = os.path.expanduser(path)
        self.config = ConfigParser.RawConfigParser()
        self.config.read(self.path)

    def edit(self, key, value, section='config'):
        cfgfile = open(self.path, 'w')
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        self.config.write(cfgfile)
        cfgfile.close()

    def list(self, section='config'):
        return self.config.items(section)

    def dump(self):
        for section in self.config.sections():
            print section
            for option in self.config.options(section):
                print " ", option, "=", self.config.get(section, option)

    def read(self, key, section='config'):
        return self.config.get(section, key)

    def load(self):
        pass

    def merge(self, config):
        # return config.update(self.list())
        return dict(self.list() + config.items())


class Utils():
    @classmethod
    def is_binary(cls, path):
        if platform.startswith('win'):
            return cls.is_binary_win(path)
        return cls.is_binary_unx(path)

    @classmethod
    def is_binary_win(cls, path):
        chrs = [7, 8, 9, 10, 12, 13, 27] + range(0x20, 0x100)
        textchars = ''.join(map(chr, chrs))
        b = open(path).read(1024)
        return bool(b.translate(None, textchars))

    @classmethod
    def is_binary_unx(cls, path):
        args = ["file", '-i', '-b', path]
        o = Popen(args, stdout=PIPE).stdout.read()
        return re.search(r'text', o) is None


class Context():
    """
    Context object that holds values to be replaced
    in templated files and paths.
    """
    def __init__(self, context_file=None):
        self.context_file = context_file
        self.load()
        config = Config()
        self.context = config.merge(self.context)
        print self.context

    def load(self):
        with open(self.context_file, 'r') as content_file:
            config = content_file.read()
            self.context = json.loads(config)
            print type(self.context)
        print("Loaded:\n {0}".format(config))

    def set_var(self, key, value):
        self.context[key] = value

    def get_context(self):
        return self.context


class Template():
    def __init__(self, context):
        self.context = context

    def replace(self, template):
        def _replace(match):
            word = match.group(1)
            return self.context.get(word, match.group())
        return re.sub(r'#(\w+)#', _replace, template)

    def compile(self, path):
        # dest = path.format(**self.context)
        dest = self.replace(path)
        pdest = os.path.dirname(dest)
        print "Dest: {}".format(pdest)
        if not os.path.isdir(pdest):
            os.makedirs(pdest)
        with open(path, 'r') as src, open(dest, 'w+') as new:
            # print src
            out = self.replace(src.read())
            # out = src.read().format(**self.context)
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
            src = os.path.join(tmp, '#__src__#')
            out = os.path.join(tmp, 'output')
            os.makedirs(src)
            #TODO: Remove zip dependency.
            call(["cp", "-R", self.src, src])
            # with zipfile.ZipFile(self.src, 'r') as zfile:
                # zfile.extractall(src)
            tfiles = self.list_files(src)
            for f in tfiles:
                print "test {}".format(f)
                if f is Utils.is_binary(f):
                    continue
                self.template.compile(f)
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
    parser = argparse.ArgumentParser(description='./bootstrapper.py -c example/bootstrap.json -t ~/.cookiejar/default/')
    parser.add_argument('-c', '--context-file',
                        dest="context_file",
                        required=True, help='Context file')
    parser.add_argument('-t', '--template',
                        default='~/.cookiejar/default/', help='Template file.')
    parser.add_argument('-o', '--output',
                        dest="output", default='.',
                        required=False, help='Output directory')
    args = parser.parse_args()

    # config.edit('author', 'goliatone')
    # config.dump()
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
