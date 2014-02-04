#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import subprocess
import os
import sys
import shutil

def ensure_path(path):
    pass


class VCS():

    def __init__(self, url=''):
        """
        https://github.com/CG-TTDET/Platform.git
        git@github.com:goliatone/minions.git

        https://goliatone@bitbucket.org/goliatone/tty2gif
        ssh://hg@bitbucket.org/goliatone/personaldetection

        @param url:
        @return:
        """
        self.url = url

    def get_handler(self, url):
        #TODO: Make this for realz
        if '.git' in url:
            return 'git'
        elif 'hg@' or 'bitbucket.org' in url:
            return 'hg'
        else:
            raise Exception


    def get_repo_name(self, url, target_dir):
        tail = url.rpartition('/')[2]
        tail = tail.replace('.git', '')
        return os.path.normpath(os.path.join(target_dir, tail))

    def notify_existing_repo(self, repo_path):
        if not os.path.isdir(repo_path):
            return
        question = "Repo '{0}' exists, want to delete and clone?".format(repo_path)
        if self.prompt_question(question):
            print "Removing '{0}'...".format(repo_path)
            shutil.rmtree(repo_path)
        else:
            print "You don't want to overwrite. Bye!"
            sys.exit(0)

    def prompt_question(self, question, default=True):
        valid = {'yes':True, 'y':True, 'no':False, 'n':False}

        prompt = '[y/n]'
        if default == True:
            prompt = '[Y/n]'
        elif default == False:
            prompt = '[y/N]'

        while True:
            sys.stdout.write("{0} {1} ".format(question, prompt))
            choice = raw_input().lower()
            if default is not None and choice == '':
                return default
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no'"\
                                 "(or 'y' or 'n')")

    def clone(self, url=None, checkout_branch=None, target_dir='.'):
        if url:
            self.url = url

        url = self.url

        #let's check target dir:
        target_dir = os.path.expanduser(target_dir)
        ensure_path(target_dir)

        #did we get a git or hg repo?
        vcs = self.get_handler(url)
        print vcs

        repo_path = self.get_repo_name(url, target_dir)
        print repo_path

        if os.path.isdir(repo_path):
            self.notify_existing_repo(repo_path)

        subprocess.check_call([vcs, 'clone', url], cwd=target_dir)

        if checkout_branch:
            subprocess.check_call([vcs, 'checkout', checkout_branch], cwd=target_dir)

        return repo_path
