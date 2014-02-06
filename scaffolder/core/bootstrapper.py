#!/usr/bin/env python
# -*- coding: utf-8 -*-
# http://stackoverflow.com/questions/15583870/mixing-positional-and-optional-arguments-in-argparse
import json
import tempfile
import contextlib
import shutil
import os
import re
import glob
import yaml
from scaffolder.core.utils import Utils, cp_recursive, commonprefix
from scaffolder.core.config import Config
from scaffolder.core.hook import HookRunner

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

    def move_to_target(self,project_template=None, target_path=None):
        cp_recursive(project_template, target_path)

    def move_content(self, src_path=None, files=[]):
        for source, target in files.items():
           if os.path.exists(source):
               try:
                   os.rename(source, target)
               except:
                   continue

        cp_recursive(src_path+'/', self.path)


    def create_output_paths(self, tmp_dir):
        out = os.path.join(tmp_dir, 'output')

        src = os.path.join(tmp_dir, '#__src__#')
        os.makedirs(src)

        return out, src


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
        self.config = config
        self.context = config.merge(self.context)

    def load(self):
        with open(self.context_file, 'r') as content_file:
            config = content_file.read()
            self.context = json.loads(config)

    def set_var(self, key, value):
        self.context[key] = value

    def parse(self):
        return self.context


class Template():
    def __init__(self, context=None, path=None, project_dir="#project#"):
        self.context = context
        self.path = Utils.normalize_path(path)
        self.name = os.path.basename(self.path)
        self.project_dir = project_dir
        self.compiled = []
        self.binaries = {}

    def project_template(self):
        return os.path.join(self.path, self.project_dir)

    def replace(self, template):
        def _replace(match):
            word = match.group(1)
            return self.context.get(word, match.group())
        return re.sub(r'#(\w+)#', _replace, template)

    def mkdir_target(self, target=None):
        path = os.path.dirname(target)
        if not os.path.isdir(path):
            os.makedirs(path)
        return path

    def compile(self, file_paths):
        for file in file_paths:
            if Utils.is_binary(file):
                self.track_binary(file)
            else:
                self.compile_file(file)

    def compile_file(self, path):
        target_file = self.add_compiled_path(path)
        self.mkdir_target(target=target_file)
        self.replace_tokens(filename=target_file, path=path)

    def replace_tokens(self, filename=None, path=None):
        #TODO: Right now we are moving this already to the endpoint
        #we might want to keep it on tmp? and then move?
        with open(path, 'r') as template, open(filename, 'w+') as new:
            content = self.replace(template.read())
            # out = src.read().format(**self.context)
            new.write(content)

    def add_compiled_path(self, path):
        file = self.replace(path)
        self.compiled.append(file)
        return file

    def track_binary(self, file):
        path = self.add_compiled_path(file)
        self.binaries[file] = path

    def get_target_root(self):
        return os.path.basename(commonprefix(self.compiled).strip('/'))

    def join_root_to_path(self, path):
        root = self.get_target_root()
        return os.path.join(path, root)


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
        self.hook = HookRunner()
        self.output = TemplateOutput(output)
        self.context = Context(context_file)
        context = self.context.parse()
        self.template = Template(context=context, path=template_path)
        self.context.set_var('__src__', 'output')

    def create(self):
        with self.make_tmp_dir() as tmp:
            out, src = self.output.create_output_paths(tmp)

            #Copy original template files into destination.
            project_template = self.template.project_template()
            self.output.move_to_target(target_path=src,
                                       project_template=project_template)

            template_files = self.list_files(src)
            print "=" * 8
            print "\n".join(template_files)
            print "=" * 8
            # self.run_hooks(self.output.path, hook='pre')
            self.template.compile(template_files)

            self.output.move_content(files=self.template.binaries,
                                     src_path=out)

            self.clean_directory(src, out)

            cwd = self.get_target_cwd()

            self.hook.run(path=self.template.path,
                          cwd=cwd,
                          hook='post')

    def clean_directory(self, src, target):
        shutil.rmtree(src)

    def get_target_cwd(self):
        cwd = self.template.get_target_root()
        return os.path.join(self.output.path, cwd)

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
