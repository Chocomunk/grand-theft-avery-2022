import sys
import shlex

from enum import Enum
from typing import Callable, Dict, List

from logger import Logger, make_stdout_stderr
from filesystem import File, Node


# TODO: Automate command-name -> resolving command/program

class EXIT_CODES(Enum):
    OK = 0
    ERROR = 1
    EXIT = -1

# OS Commands
EXIT_CMD = "exit"
CHDIR_CMD = "cd"
LISTF_CMD = "lsf"
LISTD_CMD = "lsd"
SHOWLOG_CMD = "showlog"
UNLOCK_PASSWD_CMD = "passwd"

def exit(env, args):
    return -2

def chdir(env, args):
    if len(args) != 2:
        print("Error: {0} only accepts 1 argument!".format(CHDIR_CMD), file=sys.stderr)
        return EXIT_CODES.ERROR

    dirname = args[1]
    new_node = env.curr_node.find_neighbor(dirname)

    if not new_node:
        pwd = env.curr_node.directory.name
        print("Error: no directory named {0} connected to {1}!".format(dirname, pwd), file=sys.stderr)
        return EXIT_CODES.ERROR

    if not new_node.locked(new_node):
        env.curr_node = new_node
        new_node.call_entry_callbacks(new_node)
    else:
        print("Error: {0} is locked!".format(dirname))
        return EXIT_CODES.ERROR
    return EXIT_CODES.OK

def unlock_passwd(env, args):
    if len(args) != 3:
        print("Error: {0} must take 2 arguments!".format(UNLOCK_PASSWD_CMD), file=sys.stderr)
        return EXIT_CODES.ERROR

    dirname = args[1]
    new_node = env.curr_node.find_neighbor(dirname)

    if not new_node:
        pwd = env.curr_node.directory.name
        print("Error: no directory named {0} connected to {1}!".format(dirname, pwd), file=sys.stderr)
        return EXIT_CODES.ERROR
    
    if not new_node.passlocked:
        print("Error: directory {0} is not password-locked (something else?)".format(dirname), file=sys.stderr)
        return EXIT_CODES.ERROR

    if new_node.try_password(args[2]):
        print("Success! {0} is unlocked.".format(dirname))
    else:
        print("Incorrect password for {0}".format(dirname), file=sys.stderr)
    return EXIT_CODES.OK

def list_files(env, args):
    if len(args) != 1:
        print("Error: {0} does not take any arguments".format(LISTF_CMD), file=sys.stderr)
        return EXIT_CODES.ERROR
    print(env.curr_node.directory.list_dir())
    return EXIT_CODES.OK

def list_dirs(env, args):
    if len(args) != 1:
        print("Error: {0} does not take any arguments".format(LISTD_CMD), file=sys.stderr)
        return EXIT_CODES.ERROR
    print(env.curr_node.list_children())
    return EXIT_CODES.OK


class ENV:

    def __init__(self):
        self.prompt_base = "[{pwd}]> "
        self.path: Dict[str, File] = {}

        self.curr_node: Node = None
        self.node_history: List[Node] = []


# TODO: Validate arg[i] values for every shell command
# TODO: Prettify list outputs
class Shell:

    def __init__(self, root: Node):
        # Setup logger. NOTE: If other shells become active, they will take over output
        self.stdout, self.stderr = make_stdout_stderr()
        sys.stdout = self.stdout
        sys.stderr = self.stderr

        # Initialize FS and ENV
        self.root = root
        self.env = ENV()
        self.env.curr_node = root

    def print_log(self, env, args):
        if len(args) > 2:
            print("Error: {0} takes up to 1 argument".format(SHOWLOG_CMD), file=sys.stderr)
            return EXIT_CODES.ERROR
        start_i = 0 if len(args) == 1 else args[1]
        print(self.stdout.get(start_i))
        return EXIT_CODES.OK

    def handle_input(self, inp):
        # Log CLI input
        self.stdout.log_cli(self.prompt() + inp)

        # Split and check input
        args = shlex.split(inp)
        if len(args) == 0:
            return True
        
        # Parse commands
        # TODO: see if we can standardize command parameters so that everything 
        #       can go in a dict for easy command checking
        # TODO: handle exit codes
        if args[0] == EXIT_CMD:
            exit(self.env, args)
            return False # TODO: handle exit codes properly.
        elif args[0] == CHDIR_CMD:
            chdir(self.env, args)
        elif args[0] == LISTF_CMD:
            list_files(self.env, args)
        elif args[0] == LISTD_CMD:
            list_dirs(self.env, args)
        elif args[0] == SHOWLOG_CMD:
            self.print_log(self.env, args)
        elif args[0] == UNLOCK_PASSWD_CMD:
            unlock_passwd(self.env, args)
        else:
            print("Error: unknown command/program '{0}'".format(args[0]), file=sys.stderr)
        return True

    def prompt(self):
        return self.env.prompt_base.format(pwd=self.env.curr_node.directory.name)

