#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from optparse import OptionParser
from scaffolder import get_minion_path
from scaffolder.core.template import TemplateManager
from scaffolder.core.commands import BaseCommand

class InstallCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "-t",
            "--target",
            dest="target_dir",
            default=get_minion_path('weaver'),
            help='Project Templates directory.',
            metavar="TEMPLATES_DIR"
        ),
    )

    help = 'Installs a Project Template.'


    def run(self, *args, **options):
        src = args[0]
        tgt = options.get('target_dir')

        manager = TemplateManager()
        manager.install(src=src, dest=tgt)
