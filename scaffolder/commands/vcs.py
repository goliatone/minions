#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from scaffolder.cli import BaseCommand
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
    def run(self, *args, **options):
        url = options.get('url')
        tgt = options.get('output')

        boot = VCS(url)
        boot.clone(target_dir=tgt)
