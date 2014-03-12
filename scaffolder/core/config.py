#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import os

class Config():
    #TODO: Remove hardcoded config path!
    def __init__(self, path='~/.minions/weaver/.config'):

        self.path = path

        if '~' in path:
            self.path = os.path.expanduser(path)


        if not os.path.isfile(self.path):
            print "File {0} does not exist".format(self.path)

        print "Config loading {0}".format(path)
        self.config = ConfigParser.RawConfigParser()
        ok = self.config.read(self.path)
        # fp = open(self.path)

        print "Read file: {0}".format(ok)
        # print "Config: {0}".format(self.config.get('author', 'config'))
        # self.list()

    def edit(self, key, value, section='config'):
        try:
            cfgfile = open(self.path, 'w')
        except Exception:
            print "Error"
            return

        if not self.config.has_section(section):
            self.config.add_section(section)

        if value == None:
            self.config.remove_option(section, key)
        else:
            self.config.set(section, key, value)

        self.config.write(cfgfile)
        cfgfile.close()

    def list(self, section='config'):
        print "Config list: {0}".format(section)
        if self.config.has_section(section):
            return self.config.items(section)
        return dict()

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
        print "Config merge: {0}".format(config)
        if not self.config.has_section('config'):
            return config
        return dict(self.list() + config.items())
