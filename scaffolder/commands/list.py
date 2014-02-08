#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from optparse import OptionParser
from scaffolder.core.commands import BaseCommand
from scaffolder.core.template import TemplateManager

class TemplateCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "-u",
            "--url",
            dest="url",
            default='default',
            help='Database router id.',
            metavar="DATABASE"
        ),
    )

    def __init__(self, name, help='', aliases=(), stdout=None, stderr=None):
        help = 'Template command help entry'
        parser = OptionParser(
            version=self.get_version(),
            option_list=self.get_option_list(),
            usage='\n  %prog {0} [OPTIONS] FILE...'.format(name)
        )
        aliases = ('tmp',)
        BaseCommand.__init__(self, name, parser=parser, help=help, aliases=aliases)

    def run(self, *args, **options):
        url = options.get('url')
        debug = options.get('debug')
        manger = TemplateManager()
        manger.list()
        print "Execute template {0}, {1}".format(url, debug)

