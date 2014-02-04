#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from optparse import OptionParser

from scaffolder.core.commands import BaseCommand
from scaffolder.core.bootstrapper import Bootstrapper


class CreateCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
           '-c',
           '--context-file',
           dest="context_file",
           help='Context file',
           metavar="CONTEXT FILE"
        ),

        make_option(
           '-t',
           '--template',
           default='~/.cookiejar/default/',
           help='Project Template file. Default to ~/.cookiejar/default',
           metavar="TEMPLATE"
        ),
        make_option(
            '-o',
            '--output',
            dest="output",
            default='.',
            help='Output directory'
        ),
    )

    def __init__(self, name, parser=None, help='', aliases=(), stdout=None, stderr=None):
        help = 'Command to create project from a Project Template.'
        aliases = ()
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
        out = options.get('output')
        tpl = options.get('template')
        ctx = options.get('context_file')

        boot = Bootstrapper()
        boot.config(template=tpl,
                    output=out,
                    context_file=ctx
        )
        boot.create()
        # boot.context.config.edit('kiko', None)
