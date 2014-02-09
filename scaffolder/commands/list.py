#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from optparse import OptionParser
from scaffolder.core.commands import BaseCommand
from scaffolder.core.template import TemplateManager

class ListCommand(BaseCommand):

    help = 'Template command help entry'

    def run(self, *args, **options):
        manger = TemplateManager()
        manger.list()

    def get_default_option(self):
        return []
