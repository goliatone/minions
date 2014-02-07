#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from optparse import OptionParser
from scaffolder.core.template import TemplateManager
from scaffolder.core.commands import BaseCommand

class InstallCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "-t",
            "--target",
            dest="target_dir",
            default='~/.cookiejar',
            help='Project Templates directory.',
            metavar="TEMPLATES_DIR"
        ),
    )

    def __init__(self, name, help='', aliases=(), stdout=None, stderr=None):
        help = 'install: Installs a Project Template.'
        parser = OptionParser(
            version=self.get_version(),
            option_list=self.get_option_list(),
            usage='\n  %prog {0} ACTION [OPTIONS]'.format(name)
        )
        aliases = ('tmp',)
        BaseCommand.__init__(self, name, parser=parser, help=help, aliases=aliases)

    def run(self, *args, **options):
        src = args[0]
        tgt = options.get('target_dir')

        manager = TemplateManager()
        manager.install(src=src, dest=tgt)
