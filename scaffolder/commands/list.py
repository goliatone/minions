#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from optparse import OptionParser
from scaffolder.core.commands import BaseCommand
from scaffolder.core.template import TemplateManager

class ListCommand(BaseCommand):

    def __init__(self, name, help='', aliases=(), stdout=None, stderr=None):
        help = 'Template command help entry'
        parser = OptionParser(
            version=self.get_version(),
            option_list=self.get_option_list(),
            usage='\n  %prog {0} [OPTIONS]'.format(name)
        )
        aliases = ('tmp',)
        BaseCommand.__init__(self, name, parser=parser, help=help, aliases=aliases)

    def run(self, *args, **options):
        manger = TemplateManager()
        manger.list()

    def get_default_option(self):
        return []
