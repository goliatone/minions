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
            help='Clone URL, it can be SSH or HTTPS. Git only for now.',
            metavar="REPO_URL"
        ),

        make_option(
            "-t",
            "--target",
            dest="target",
            default='.',
            help="Target directory where the repo will be cloned.",
            metavar="TARGET"
        ),
    )
    class Meta():
        description = 'hola'
        help = 'something goes here'

    def __init__(self, name, parser=None, help='', aliases=(), stdout=None, stderr=None):
        help = 'Command to clone github repos'
        aliases = ('git','hg',)
        #TODO: Move to BaseCommand, create methods and have each subcommand override
        parser = OptionParser(
            version=self.get_version(),
            option_list=self.get_option_list(),
            usage='\n  %prog {0} [OPTIONS] FILE...'.format(name),
            description='',
            epilog=''

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
        tgt = options.get('target')

        boot = VCS(url)
        boot.clone(target_dir=tgt)
