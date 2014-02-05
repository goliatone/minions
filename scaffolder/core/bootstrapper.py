#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/15583870/mixing-positional-and-optional-arguments-in-argparse
import json
import tempfile
import contextlib
import shutil
import os
from subprocess import call, Popen
import re
from scaffolder.core.utils import Utils
from scaffolder.core.config import Config
import glob
import yaml

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

class TemplateOutput():
    def __init__(self, path):
        self.set_path(path)

    def set_path(self, path=None):
        if not path:
            return
        self.path = Utils.normalize_path(path, mkdir=True)


    def move_content(self, src_path=None):
        call(["cp", "-R", src_path+'/', self.path])


class ProjectTemplate():
    def __init__(self, base_path='~/.cookiejar', default='default', metadata={}):
        self.name = default
        self.meta = metadata
        self.base_path = base_path

    def load(self):
        pass
    def set_path(self, path=None):
        if not path:
            return
        self.base_path = path

    def load_metadata(self, path=None):
        if path:
            self.set_path(path)
        init_file = self.get_path(append=ProjectTemplate.INIT_FILE)
        file = glob.glob(init_file)
        if file:
            content = open(file[0], 'r').readlines()
            b = [i for i in range(len(content)) if content[i] == '"""\n']
            if b.__len__() != 2:
                return
            content = "".join(content[b[0] + 1:b[1]])
            self.metadata[self.name] = yaml.load(content)

    def get_path(self, append=''):
        return os.path.realpath(os.path.join(self.base_path, self.name, append))


class Context():
    """
    Context object that holds values to be replaced
    in templated files and paths.
    """
    def __init__(self, context_file=None):
        #@todo: Normalize path! realpath/expanduser
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

    def parse(self):
        return self.context


class Template():
    def __init__(self, context=None, path=None):
        self.context = context
        self.path = Utils.normalize_path(path)
        self.name = os.path.basename(self.path)

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

    def compile_file_paths(self, file_paths):
        for f in file_paths:
            if f is Utils.is_binary(f):
                continue
            self.compile(f)

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
    def config(self, template_path=None, context_file=None, output=None):
        print "Bootstrapper: {}".format(template_path)
        self.output = TemplateOutput(output)

        self.context = Context(context_file)

        context = self.context.parse()

        self.template = Template(context=context, path=template_path)

        self.context.set_var('__src__', 'output')

    def create(self):
        print "Creating bootstrap, for template '{}'".format(self.template.name)
        with self.make_tmp_dir() as tmp:
            out = os.path.join(tmp, 'output')
            src = os.path.join(tmp, '#__src__#')
            os.makedirs(src)

            call(["cp", "-R", self.template.path, src])

            template_files = self.list_files(src)
            print "----"
            print "\n".join(template_files)
            print "----"
            # self.run_hooks(self.output.path, hook='pre')
            self.template.compile_file_paths(template_files)

            self.clean_directory(src, out)

            self.output.move_content(src_path=out)

            self.run_hooks(self.template.path, self.output.path, hook='post')

    def clean_directory(self, src, target):
        shutil.rmtree(src)
        #we should remove __init__ from target
        print "Clean target temp directory: {}".format(target)
        #we should remove hooks



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
            for f in files:
                output.append('{}/{}'.format(root, f))
        return output
    
    @contextlib.contextmanager
    def make_tmp_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
