#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sys
from optparse import OptionParser
from optparse import make_option
from scaffolder.core.utils import import_class
from scaffolder.core.optparser import CommandMeta

COMMANDS = [
    'bootstrap',
    'template',
    'config',
    'vcs'
]

class CommandController():

    DEFAULT_ARGUMENT = ['--help']

    def __init__(self, stdout=None, stderr=None):
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

        self.prog = ''
        self.command = ''
        self.argv = ()


    def execute(self, argv=None):
        argv = sys.argv if not argv else argv

        if len(argv) == 1:
            return self.show_help()

        self.parse_argv(argv)

        command = self.command
        arguments = self.argv
        self.run_command(command, arguments)

    def run_command(self, cmd, argv):
        try:
            Command = self.get_command_class(cmd)
        except Exception, e:
            self.exception_handler(e)

        command = Command(stdout=self.stdout, stderr=self.stderr, cmd=cmd)
        command.run_from_argv(argv)

    def parse_argv(self, argv):
        self.argv = argv
        # This should always be here
        self.prog = argv[0]
        #Expect subcommand else would have show_help
        self.command = argv[1]
        # We want to store the arguments or show help
        self.argv = argv[2:] or CommandController.DEFAULT_ARGUMENT

    def get_command_class(self, cmd):
        try:
            #module name
            module  = cmd.lower()
            #class name
            Command = "{0}Command".format(module.title())
            cmd_path = 'scaffolder.commands.' + module+'.'+Command
            print "Command path {0}".format(cmd_path)

            if isinstance(cmd_path, basestring):
                Command = import_class(cmd_path)

            return Command

        except Exception, e:
            print "Error"
            self.exception_handler(e)

    def exception_handler(self, e):
        self.stderr.write(str(e)+'\n')
        self.show_help()
        sys.exit(-1)

    def show_help(self):
        output = [
            'Usage %s subcommand [options] [args]' % self.command,
            '',
            'Available commands:',
            '',
        ]

        for cmd in COMMANDS:
            output.append(' %s' % cmd)

        output += ['', '']
        self.stdout.write(u'\n'.join(output))


class BaseCommand():
    help = ''
    args = ''
    option_list = (
        make_option('--debug', action='store_true', dest='debug',
                    default=False, help='Debug mode'),
        make_option('--traceback', action='store_true', dest='traceback',
                    default=True, help='Print traceback in error')
    )

    def __init__(self, stdout=None, stderr=None, cmd=None, parser=None):
        self.cmd = cmd
        self.meta = CommandMeta(cmd, parser, self.help)
        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

    def execute(self, *args, **options):
        try:
            self.run(*args, **options)
        except Exception, e:
            if options['debug']:
                # sys.stderr.write(colorize('ERROR: ', fg='red'))
                self.stderr.write('%s\n' % e)
                sys.exit(1)
            else:
                raise
    def get_option_list(self):
        return self.option_list

    def get_parser(self, prog_name, subcommand):
        print "Prog name {0}".format(prog_name)
        parser = OptionParser(
            prog=subcommand,
            usage=self.get_usage(),
            version=self.get_version(),
            option_list=sorted(self.get_option_list())
        )
        return parser

    def get_usage(self):
        return "%prog command"

    def get_version(self):
        from scaffolder import get_version
        return get_version()

    def print_help(self, prog_name, subcommand):
        parser = self.get_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        parser = self.get_parser(sys.argv[0], sys.argv[1])
        options, args = parser.parse_args(argv)
        self.execute(*args, **options.__dict__)
        # self.execute(argv)

    def run(self, *args, **options):
        raise NotImplementedError()