#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
from optparse import make_option

COMMANDS = [
    'bootstrap',
    'template',
    'config',
    'vcs'
]

class CommandController():
    def __init__(self, argv=None, stdout=None, stderr=None):
        if not argv:
            argv = sys.argv
        self.prog = argv[0]
        self.command = argv[1]
        self.argv = argv[2:]

        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

    def execute(self):
        if not len(self.argv):
            return self.show_help()

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

    def __init__(self, stdout=None, stderr=None, cmd=None):
        self.cmd = cmd
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
        parser = OptionParser(
            prog=prog_name,
            # usage=self.usage(),
            # version=self.version(),
            option_list=sorted(self.get_option_list())
        )
        return parser

    def print_help(self, prog_name, subcommand):
        parser = self.get_parser(prog_name, subcommand)
        parser.print_help()

    def run_from_argv(self, argv):
        parser = self.get_parser(argv[0], argv[1])
        options, args = parser.parse_args(sys.argv[2:])
        self.execute(*args, **options.__dict__)
        # self.execute(argv)

    def run(self, *args, **options):
        raise NotImplementedError()


def import_class(class_path):
    segments = class_path.split('.')
    module = '.'.join(segments[:-1])
    class_name = segments[-1]
    try:
        module = __import__(module, {}, {}, [class_name])
    except ImportError, err:
        msg = "There was problem while trying to import class. "\
            "Original error was:\n%s" % err
        raise Exception(msg)
    Class = getattr(module, class_name)

    return Class
