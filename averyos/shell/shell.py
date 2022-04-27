from ast import arg
from multiprocessing.dummy import current_process
import sys
import shlex
import traceback

from .env import ENV
from system.filesystem import Node
from .copy_logger import get_stdio_loggers
from system.usrbin_programs import usrbin_progs
from system.program import ExitCode, CLIProgramBase


class UnknownProgram(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
        print("Error: unknown command/program '{0}'".format(args[0]), file=sys.stderr)
        return ExitCode.ERROR


# TODO: move this somewhere else once callbacks are figured out
def sheesh_split(s: str):
    """ Put a space between the 'sh' and 'eesh' """
    if s.startswith('sh'):
        return 'sh ' + s[2:]
    return s


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
        # Preprocess inputs
        # TODO: Add callbacks for puzzles to take control
        inp = sheesh_split(inp)
        
        # Split and check input
        args = shlex.split(inp)
        if len(args) == 0:
            return True
        
        # Parse commands
        prog = self.unknown_program     # Default to unknown

        # Check programs in CWD
        if args[0] in ENV.curr_node.directory.programs:
            prog = ENV.curr_node.directory.programs[args[0]]

        # Check programs in path
        elif args[0] in ENV.path:
            prog = ENV.path[args[0]]

        # TODO: handle GUI execution
        try:
            errcode = prog.cli_main(args)
        except Exception:               # Catch program errors then continue
            traceback.print_exc()
            errcode = ExitCode.ERROR

        if errcode == ExitCode.EXIT:
            return False
        return True

