#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
from optparse import make_option
import textwrap


class CommandMeta(object):
    """A subcommand of a root command-line application that may be
    invoked by a SubcommandOptionParser.
    """
    def __init__(self, name, parser=None, help='', aliases=()):
        """Creates a new subcommand. name is the primary way to invoke
        the subcommand; aliases are alternate names. parser is an
        OptionParser responsible for parsing the subcommand's options.
        help is a short description of the command. If no parser is
        given, it defaults to a new, empty OptionParser.
        """
        self.name = name

        self.help = help

        self.aliases = aliases

        self.parser = parser or optparse.OptionParser()

        self.option_list = ()

    def get_option_list(self):
        return sorted(self.option_list, reverse=True)

class CommandOptionParser(optparse.OptionParser):
    """A variant of OptionParser that parses commands and their
    arguments.
    """

    # A singleton command used to give help on other commands.
    _HelpCommandMeta = CommandMeta('help', optparse.OptionParser( ),
        help='give detailed help on a specific sub-command',
        aliases=('?',))

    def __init__(self, *args, **kwargs):
        """Create a new subcommand-aware option parser. All of the
        options to OptionParser.__init__ are supported in addition
        to commands, a sequence of CommandMeta objects.
        """
        # The subcommand array, with the help command included.
        self.commands = list(kwargs.pop('commands', []))
        self.commands.append(self._HelpCommandMeta)

        # A more helpful default usage.
        if 'usage' not in kwargs:
            kwargs['usage'] = self.make_usage()
        # Super constructor.
        optparse.OptionParser.__init__(self, *args, **kwargs)

        # Our root parser needs to stop on the first unrecognized argument.
        self.disable_interspersed_args()

    def make_usage(self):
        usage = """
  %prog MINION [ARGS...]
  %prog help MINION
      """
        return usage

    def add_subcommand(self, cmd, index=0):
        """Adds a CommandMeta object to the parser's list of commands.
        """
        self.commands.insert(index, cmd)

    # Add the list of commands to the help message.
    def format_help(self, formatter=None):
        # Get the original help message, to which we will append.
        out = optparse.OptionParser.format_help(self, formatter)

        # out = 'THIS IS A HEADER, IT SHOULD GO HERE\n'+out

        if formatter is None:
            formatter = self.formatter

        # Subcommands header.
        result = ["\n"]
        result.append(formatter.format_heading('Commands'))
        formatter.indent()

        # Generate the display names (including aliases).
        # Also determine the help position.
        disp_names = []
        help_position = 0
        for subcommand in self.commands:
            name = subcommand.name
            if subcommand.aliases:
                name += ' (%s)' % ', '.join(subcommand.aliases)
            disp_names.append(name)

            # Set the help position based on the max width.
            proposed_help_position = len(name) + formatter.current_indent + 2
            if proposed_help_position <= formatter.max_help_position:
                help_position = max(help_position, proposed_help_position)

        # Add each subcommand to the output.
        for subcommand, name in zip(self.commands, disp_names):
            # Lifted directly from optparse.py.
            name_width = help_position - formatter.current_indent - 2
            if len(name) > name_width:
                name = "%*s%s\n" % (formatter.current_indent, "", name)
                indent_first = help_position
            else:
                name = "%*s%-*s  " % (formatter.current_indent, "",
                                      name_width, name)
                indent_first = 0
            result.append(name)
            help_width = formatter.width - help_position
            help_lines = textwrap.wrap(subcommand.help, help_width)
            result.append("%*s%s\n" % (indent_first, "", help_lines[0]))
            result.extend(["%*s%s\n" % (help_position, "", line)
                           for line in help_lines[1:]])
        formatter.dedent()

        # Concatenate the original help message with the subcommand
        # list.
        return out + "".join(result)

    def _subcommand_for_name(self, name):
        """Return the subcommand in self.commands matching the
        given name. The name may either be the name of a subcommand or
        an alias. If no subcommand matches, returns None.
        """
        for subcommand in self.commands:
            if name == subcommand.name or \
               name in subcommand.aliases:
                return subcommand
        return None

    def exit_with_help(self):
        self.print_help()
        self.exit()

    def parse_args(self, a=None, v=None):
        """Like OptionParser.parse_args, but returns these four items:
        - options: the options passed to the root parser
        - subcommand: the CommandMeta object that was invoked
        - suboptions: the options passed to the subcommand parser
        - subargs: the positional arguments passed to the subcommand
        """
        options, args = optparse.OptionParser.parse_args(self, a, v)

        if not args:
            # No command given.
            self.exit_with_help()
        else:
            cmd = args.pop(0)
            subcommand = self._subcommand_for_name(cmd)
            if not subcommand:
                self.error('unknown command ' + cmd)

        suboptions, subargs = subcommand.parser.parse_args(args)

        #we entered "help" command:
        if subcommand is self._HelpCommandMeta:
            if subargs:
                # particular
                cmd = subargs[0]
                help_cmd = self._subcommand_for_name(cmd)
                help_cmd.parser.print_help()
                self.exit()
            else:
                # general
               self.exit_with_help()

        return options, subcommand, suboptions, subargs
