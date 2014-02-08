#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from optparse import OptionParser
import os
from scaffolder import get_minion_path
from scaffolder.core.commands import BaseCommand
from scaffolder.core.bootstrapper import Bootstrapper

"""
create PROJECT_TEMPLATE [-c CONTEXT_FILE|def] [-o OUTPUT_DIR]
- We need project template name. We then need to check and see
if its available. Else, throw up.
- If we do not provide a context path, we look for context.json
or project_template.json on same dir.
- We can provide output dir. Else on same directory.
"""
class CreateCommand(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
           '-c', '--context-file', dest="context_file",
           metavar="CONTEXT_FILE", help='Context file',
        ),
        make_option(
           '-t', '--template_path',
           default=get_minion_path('weaver'), metavar="TEMPLATE_PATH",
           help='Project Template file. Default to %s' % get_minion_path('weaver')
        ),
        make_option(
            '-o', '--output', dest="output", default='.',
            help='Output directory'
        ),
    )

    def __init__(self, name, help='', aliases=(), stdout=None, stderr=None):
        help = 'Command to create project from a Project Template.'
        aliases = ()
        #TODO: Move to BaseCommand, create methods and have each subcommand override
        parser = OptionParser(
            version=self.get_version(),
            option_list=self.get_option_list(),
            usage=self.get_usage(name),
            description='',
            epilog=''
        )
        BaseCommand.__init__(self, name, parser=parser, help=help, aliases=aliases)

    def get_usage(self, name):
        return '\n  %prog {0} TEMPLATE_NAME [OPTIONS]\n \
                        TEMPLATE_NAME must be the name of a registered\n \
                        template project.'.format(name)

    def validate_path(self, path):
        if not os.path.exists(path):
            self.exit_with_help("Path to output must be a valid path {}".format(path))

    def run(self, *args, **options):
        output = options.get('output')
        path = options.get('template_path')
        context = options.get('context_file')

        self.validate_path(output)

        try:
            tpl_name = args[0]
            template = os.path.join(path, tpl_name)
            #TODO: Validate that we have a real template
        except:
            self.exit_with_help("Missing project template name.\n")

        boot = Bootstrapper()
        boot.config(template_path=template,
                    output=output,
                    context_file=context
        )

        boot.create()
        # boot.context.config.edit('kiko', None)
