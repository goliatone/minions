#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from subprocess import call, Popen

#TODO: Make this for realz!
class HookRunner():

    def run(self, path=None, cwd=None, hook='post'):
        script = os.path.join(path, 'hooks', hook)
        if not os.path.isfile(script):
            return
        try:
            print "Executing in context {0}".format(cwd)
            Popen(script, cwd=cwd)

        except Exception, e:
            print e
