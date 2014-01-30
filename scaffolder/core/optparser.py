#!/usr/bin/env python
# -*- coding: utf-8 -*-

import optparse
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
            kwargs['usage'] = """
  %prog COMMAND [ARGS...]
  %prog help COMMAND"""
        kwargs['description'] = "Hola %prog, not sure what is this"
        # Super constructor.
        optparse.OptionParser.__init__(self, *args, **kwargs)

        # Adjust the help-visible name of each subcommand.
        for subcommand in self.commands:
            subcommand.parser.prog = '%s %s' % \
                    (self.get_prog_name(), subcommand.name)

        # Our root parser needs to stop on the first unrecognized argument.
        self.disable_interspersed_args()

    def add_subcommand(self, cmd):
        """Adds a CommandMeta object to the parser's list of commands.
        """
        self.commands.append(cmd)

    # Add the list of commands to the help message.
    def format_help(self, formatter=None):
        # Get the original help message, to which we will append.
        out = optparse.OptionParser.format_help(self, formatter)
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
            self.print_help()
            self.exit()
        else:
            cmdname = args.pop(0)
            subcommand = self._subcommand_for_name(cmdname)
            if not subcommand:
                self.error('unknown command ' + cmdname)

        suboptions, subargs = subcommand.parser.parse_args(args)

        if subcommand is self._HelpSubcommand:
            if subargs:
                # particular
                cmdname = subargs[0]
                helpcommand = self._subcommand_for_name(cmdname)
                helpcommand.parser.print_help()
                self.exit()
            else:
                # general
                print "HERE {0}".format(subcommand)
                self.print_help()
                self.exit()

        return options, subcommand, suboptions, subargs

# Smoke test.
if __name__ == '__main__':
    # Some commands.
    add_cmd = CommandMeta('add',
        optparse.OptionParser(usage='%prog [OPTIONS] FILE...'),
        'add the specified files on the next commit')

    add_cmd.parser.add_option('-n', '--dry-run', dest='dryrun',
        help='do not perform actions, just print output',
        action='store_true')

    commit_cmd = CommandMeta('commit',
        optparse.OptionParser(usage='%prog [OPTIONS] [FILE...]'),
        'commit the specified files or all outstanding changes',
        ('ci',))

    # A few dummy commands for testing the help layout algorithm.
    long_cmd = CommandMeta('very_very_long_command_name',
        optparse.OptionParser(),
        'description should start on next line')
    long_help_cmd = CommandMeta('somecmd', optparse.OptionParser(),
        'very long help text should wrap to the next line at which point '
        'the indentation should match the previous line',
        ('history',))

    # Set up the global parser and its options.
    parser = CommandOptionParser(
        commands = (add_cmd, commit_cmd, long_cmd, long_help_cmd)
    )
    parser.add_option('-R', '--repository', dest='repository',
                      help='repository root directory or symbolic path name',
                      metavar='PATH')
    parser.add_option('-v', dest='verbose', help='enable additional output',
                      action='store_true')

    # Parse the global options and the subcommand options.
    options, subcommand, suboptions, subargs = parser.parse_args()

    # Here, we dispatch based on the identity of subcommand. Of course,
    # one could instead add a "func" property to all the commands
    # and here just call subcommand.func(suboptions, subargs) or
    # something.
    if subcommand is add_cmd:
        if subargs:
            print 'Adding files:', ', '.join(subargs)
            print 'Dry run:', ('yes' if suboptions.dryrun else 'no')
        else:
            # Note that calling error() on the subparser is the right
            # thing to do here. This way, the usage message reflects
            # the subcommand's usage specifically rather than just the
            # root command.
            subcommand.parser.error('need at least one file to add')
    elif subcommand is commit_cmd:
        if subargs:
            print 'Committing files:', ', '.join(subargs)
        else:
            print 'Committing all changes.'
    else:
        print '(dummy command)'

    # Show the global options.
    print 'Repository:', (options.repository if options.repository
                          else '(default)')
    print 'Verbose:', ('yes' if options.verbose else 'no')
