#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from optparse import OptionParser

from scaffolder.core.commands import BaseCommand
from scaffolder.vcs import VCS


class VcsCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "-u",
            "--url",
            dest="url",
            default='default',
            help='Database router id.',
            metavar="DATABASE"
        ),

        make_option(
            "-o",
            "--output",
            dest="output",
            default='.',
            help="S3 bucket name",
            metavar="BUCKET"
        ),
    )
    class Meta():
        description = 'hola'
        help = 'something goes here'

    def __init__(self, name, parser=None, help='', aliases=(), stdout=None, stderr=None):
        help = 'VCS command help entry'
        aliases = ('git','hg',)
        parser = OptionParser(
            version=self.get_version(),
            option_list=self.get_option_list(),
            usage='\n  %prog {0} [OPTIONS] FILE...'.format(name)
        )
        BaseCommand.__init__(self, name, parser=parser, help=help, aliases=aliases)
        # self.update_parser()

    def update_parser(self):
        self.parser.set_usage('%prog [OPTIONS] FILE...')
        # self.parser.prog = '%s %s' % (self.parser.get_prog_name(), self.name)
        self.parser.version = self.get_version()
        self.parser.option_list = sorted(self.get_option_list())



    def run(self, *args, **options):
        url = options.get('url')
        tgt = options.get('output')

        boot = VCS(url)
        boot.clone(target_dir=tgt)
