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

    help = 'Command to clone github repos'

    def run(self, *args, **options):
        url = options.get('url')
        tgt = options.get('target')

        boot = VCS(url)
        boot.clone(target_dir=tgt)
