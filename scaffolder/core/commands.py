#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import make_option
from scaffolder.core.utils import import_class
from scaffolder.core.optparser import CommandMeta
from scaffolder.core.optparser import CommandOptionParser
from scaffolder import get_version
from clint.textui.colored import red



class CommandController():

    DEFAULT_ARGUMENT = ['--help']

    def __init__(self, stdout=None, stderr=None):

        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

        #Hold a ref to all Cmd's id
        self.command_ids = []

        self.prog = ''
        self.command = ''
        self.argv = ()

        #Make CliApplication, instantiate a new CommandController and set
        self.description = "The program %prog has the following commands"
        self.parser = CommandOptionParser(description=self.description)


    def register_command_names(self, command_names):
        """
        Note that we insert instead of append to list
        the commands in help as they were introduced.
        TODO: Add support for aliases(?)
        @param command_names: list of command names
        @return: void
        """
        for id in command_names:
            self.command_ids.insert(0, id)

    def execute(self, argv=None):
        argv = sys.argv if not argv else argv

        #TODO: We might want to use default command!!
        if len(argv) == 1:
            return self.show_help()
        command, arguments = self.parse_argv(argv)

        self.run_command(command, arguments)

    def run_command(self, cmd, argv):
        try:
            Command = self.get_command_class(cmd)
        except Exception, e:
            self.exception_handler(e)

        command = Command(cmd, stdout=self.stdout, stderr=self.stderr)
        command.run_from_argv(argv)

    def parse_argv(self, argv):
        # This should always be here
        self.prog = argv[0]
        #Expect subcommand else would have show_help
        self.command = argv[1]
        # We want to store the arguments or show help
        self.argv = argv[2:] or CommandController.DEFAULT_ARGUMENT
        return self.command, self.argv

    def get_command_class(self, cmd):
        try:
            #module name
            module  = cmd.lower()
            #class name
            command = "{0}Command".format(module.title())
            cmd_path = self.build_command_package(module, command)

            if isinstance(cmd_path, basestring):
                Command = import_class(cmd_path)

            return Command

        except Exception, e:
            #TODO: Here we should try to load all Commands and
            #get their aliases. OR Register the alias as well.
            self.exception_handler(e)

    def build_command_package(self, module, command):
        return 'scaffolder.commands.' + module+'.'+command

    def exception_handler(self, e):
        self.stderr.write(str(e)+'\n')
        self.show_help()
        sys.exit(-1)

    def show_help(self, load_commands=True):
        #let's load all registered commands and register them

        for cmd in self.command_ids:
            Command = self.get_command_class(cmd)
            command = Command(cmd)
            self.parser.add_subcommand(command)

        return self.stdout.write(self.parser.format_help())


class BaseCommand(CommandMeta):
    option_list = (
            make_option('--debug',
                        action='store_true',
                        dest='debug',
                        default=False,
                        help='Debug mode'
            ),
            make_option('--traceback',
                        action='store_true',
                        dest='traceback',
                        default=True,
                        help='Print traceback in error'
            )
        )

    class Meta():
        help = 'something goes here'
        description = 'hola'

    def __init__(self, name, parser=None, help='', aliases=(), stdout=None, stderr=None):

        self.stdout = stdout or sys.stdout
        self.stderr = stderr or sys.stderr

        CommandMeta.__init__(self, name, parser=parser, help=help, aliases=aliases)

    def get_meta(self):
        return

    def get_version(self):
        return get_version()

    def execute(self, *args, **options):
        try:
            self.run(*args, **options)
        except Exception, e:
            if options['debug']:
                self.stderr.write(red('%s\n' % e))
                sys.exit(1)
            else:
                raise

    def run_from_argv(self, argv):
        # parser = self.get_parser(sys.argv[0], sys.argv[1])
        parser = self.parser
        options, args = parser.parse_args(argv)
        self.execute(*args, **options.__dict__)
        # self.execute(argv)

    def run(self, *args, **options):
        raise NotImplementedError()

    def exit_with_help(self, message=None, color=red):
        if message:
            print color(message)
        self.parser.print_help()
        self.parser.exit()
