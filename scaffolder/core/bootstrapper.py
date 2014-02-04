#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/15583870/mixing-positional-and-optional-arguments-in-argparse
import sys

import argparse
import traceback
import json
import tempfile
import contextlib
import shutil
import os
from subprocess import call, Popen
import re
from scaffolder.core.utils import Utils
from scaffolder.core.config import Config


"""
scaffolder create -c example/bootstrap.json -o /tmp/vcs/

TODO: Integrate into MinionTasks
A) Given a src template dir and a context file,
   interpolate and put in out dir.
B) Have global context, i.e username email github
C) Have templates dir @ ~/.cookiejars
D) Add new templates:
   - We clone from github // bitbucket?
   - We move from local dir.
E) Add on_created_hook.py in template src dir
F) Take -C "bower install && npm install" StopIteration(" error") cmd
G) Add exclude files.
"""

class Context():
    """
    Context object that holds values to be replaced
    in templated files and paths.
    """
    def __init__(self, context_file=None):
        self.context_file = os.path.expanduser(context_file)
        if context_file:
            self.load()
        config = Config()
        self.context = config.merge(self.context)
        self.config = config
        print "Context: {0}".format(self.context)

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
    """
    @todo: We should get the path to the target's root dir.
    @todo: Clean up after we execute hooks
    A project template should have the following structure:
    - template_name: Directory containing the Project Template
      |- __init__.py Metadata file
      |- hooks: Hooks directory
      |-#project#: Root directory to the contents of the PT.
    We need a ProjectTemplate class, to handle all that.
    We need a Hook class, to execute hooks.
    """
    def config(self, template=None, context_file=None, output=None):
        self.src = os.path.expanduser(template)
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
            # self.run_hooks(self.out_dir, hook='pre')
            for f in tfiles:
                if f is Utils.is_binary(f):
                    continue
                self.template.compile(f)

            self.clean_directory(src, out)
            self.move_content(out, self.out_dir)
            self.run_hooks(self.src, self.out_dir, hook='post')

    def clean_directory(self, src, target):
        shutil.rmtree(src)
        #we should remove __init__ from target
        print "Clean target temp directory: {}".format(target)
        #we should remove hooks

    def move_content(self, out=None, target=None):
        if not target:
            target = self.out_dir
        call(["cp", "-R", out+'/', target])

    def run_hooks(self, src, target, hook='post'):
        script = os.path.join(src, 'hooks', 'post')
        if not os.path.isfile(script):
            return
        try:
            print "Executing in context {0}".format(target)
            Popen(script, cwd=target)

        except Exception, e:
            print e


    def list_files(self, path):
        """
        @rtype : object
        @param path: 
        @return: 
        """
        output = []
        for root, dirs, files in os.walk(path):
            print('{0}/'.format(root))
            for f in files:
                output.append('{}/{}'.format(root, f))
                print('{}/{}'.format(root, f))
        return output
    
    @contextlib.contextmanager
    def make_tmp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
