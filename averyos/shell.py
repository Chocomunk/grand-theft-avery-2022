import sys
import shlex

from env import ENV
from filesystem import Node
from logger import get_stdio_loggers
from usrbin_programs import usrbin_progs
from program import ExitCode, CLIProgramBase


class UnknownProgram(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
        print("Error: unknown command/program '{0}'".format(args[0]), file=sys.stderr)
        return ExitCode.ERROR


# TODO: Validate arg[i] values for every shell command
# TODO: Prettify list outputs
class Shell:

    def __init__(self, root: Node):
        # Setup logger. NOTE: If other shells become active, they will take over output
        # All stdio loggers write to the same LogData instance
        self.stdout, self.stderr, self.stdin = get_stdio_loggers()
        sys.stdout = self.stdout
        sys.stderr = self.stderr
        sys.stdin  = self.stdin

        # Initialize FS and ENV
        ENV.reset()
        self.root = root
        ENV.curr_node = root
        ENV.log = self.stdout.log      # Same LogData as stdin and stderr
        ENV.path = usrbin_progs()

        self.unknown_program = UnknownProgram()

    def prompt(self):
        return ENV.prompt_base.format(pwd=ENV.curr_node.directory.name)

    def handle_input(self, inp):
        """
        Parses and executes a cli command.

        Returns: `True` to stay alive, `False` to exit
        """
        # Split and check input
        args = shlex.split(inp)
        if len(args) == 0:
            return True
        
        # Parse commands
        prog = self.unknown_program     # Default to unknown

        # TODO: handle cwd programs first
        if args[0] in ENV.path:         # Check path
            prog = ENV.path[args[0]]

        # TODO: handle GUI execution
        errcode = prog.cli_main(args)
        if errcode == ExitCode.EXIT:
            return False
        return True

