import sys
import shlex

from typing import Dict, List

from filesystem import File, Node
from logger import get_stdio_loggers
from sysprog import ExitCodes, SYSPROG_MAP


class ENV:

    def __init__(self):
        self.prompt_base = "[{pwd}]> "
        self.path: Dict[str, File] = {}

        self.log = None

        self.curr_node: Node = None
        self.node_history: List[Node] = []


def unknown_program(env, args):
    print("Error: unknown command/program '{0}'".format(args[0]), file=sys.stderr)
    return ExitCodes.ERROR


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
        self.root = root
        self.env = ENV()
        self.env.curr_node = root
        self.env.log = self.stdout.log      # Same LogData as stdin and stderr

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
        prog = unknown_program              # Default to unknown

        # TODO: handle cwd programs first
        if args[0] in self.env.path:        # Check path
            prog = self.env.path[args[0]]
        elif args[0] in SYSPROG_MAP:
            prog = SYSPROG_MAP[args[0]]

        errcode = prog(self.env, args)
        if errcode == ExitCodes.EXIT:
            return False
        return True

    def prompt(self):
        return self.env.prompt_base.format(pwd=self.env.curr_node.directory.name)

