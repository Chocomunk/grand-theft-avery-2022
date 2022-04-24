import sys
import shlex

from typing import Dict, List

from filesystem import Node
from logger import get_stdio_loggers
from program import ExitCode, ProgramBase,  CLIProgramBase, usrbin_progs


class ENV:

    prompt_base = "[{pwd}]> "
    path: Dict[str, ProgramBase] = {}

    log = None

    curr_node: Node = None
    node_history: List[Node] = []

    @classmethod
    def reset(cls):
        cls.prompt_base = "[{pwd}]> "
        cls.path = usrbin_progs()
        cls.log = None
        cls.curr_node = None
        cls.node_history = []


class UnknownProgram(CLIProgramBase):

    def cli_main(args):
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

        self.unknown_program = UnknownProgram()

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

        errcode = prog(args)
        if errcode == ExitCode.EXIT:
            return False
        return True

    def prompt(self):
        return ENV.prompt_base.format(pwd=ENV.curr_node.directory.name)

