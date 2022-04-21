import shlex
import argparse

from typing import Callable

from logger import Logger
from filesystem import Node


# ENVs
PROMPT_BASE = "[{pwd}]> "

# TODO: Automate command-name -> resolving command/program

# OS Commands
EXIT_CMD = "exit"
CHDIR_CMD = "cd"
LISTF_CMD = "lsf"
LISTD_CMD = "lsd"
SHOWLOG_CMD = "showlog"
UNLOCK_PASSWD_CMD = "passwd-unlock"


# TODO: Validate arg[i] values for every shell command
# TODO: Prettify list outputs
class Shell:

    def __init__(self, root: Node):
        self.root = root
        self.curr_node = root

        # Initialize logger
        self.logger: Logger = Logger()
        self.log: Callable = self.logger.log
        self.logerr: Callable = self.logger.logerr

    def chdir(self, args):
        if len(args) != 2:
            self.logerr("Error: {0} only accepts 1 argument!".format(CHDIR_CMD))
            return

        dirname = args[1]
        new_node = self.curr_node.find_neighbor(dirname)

        if not new_node:
            pwd = self.curr_node.directory.name
            self.logerr("Error: no directory named {0} connected to {1}!".format(dirname, pwd))
            return

        if not new_node.locked(new_node, self):
            self.curr_node = new_node
            new_node.call_entry_callbacks(new_node, self)
        else:
            self.logerr("Error: {0} is locked!".format(dirname))
            return

    def unlock_passwd(self, args):
        if len(args) != 3:
            self.logerr("Error: {0} must take 2 arguments!".format(UNLOCK_PASSWD_CMD))
            return

        dirname = args[1]
        new_node = self.curr_node.find_neighbor(dirname)

        if not new_node:
            pwd = self.curr_node.directory.name
            self.logerr("Error: no directory named {0} connected to {1}!".format(dirname, pwd))
            return
        
        if not new_node.passlocked:
            self.logerr("Error: directory {0} is not password-locked (something else?)".format(dirname))
            return

        if new_node.try_password(args[2]):
            self.log("Success! {0} is unlocked.".format(dirname))
        else:
            self.log("Incorrect password for {0}".format(dirname))

    def list_files(self, args):
        if len(args) != 1:
            self.logerr("Error: {0} does not take any arguments".format(LISTF_CMD))
            return
        self.log(self.curr_node.directory.list_dir())

    def list_dirs(self, args):
        if len(args) != 1:
            self.logerr("Error: {0} does not take any arguments".format(LISTD_CMD))
            return
        self.log(self.curr_node.list_children())

    def print_log(self, args):
        if len(args) > 2:
            self.logerr("Error: {0} takes up to 1 argument".format(SHOWLOG_CMD))
            return
        start_i = 0 if len(args) == 1 else args[1]
        self.log(self.logger.get(start_i))

    def handle_input(self, inp):
        # Silently log input
        self.log(self.prompt() + inp, file=None)

        # Split and check input
        args = shlex.split(inp)
        if len(args) == 0:
            return True
        
        # Parse commands
        # TODO: see if we can standardize command parameters so that everything 
        #       can go in a dict for easy command checking
        if args[0] == EXIT_CMD:
            return False
        elif args[0] == CHDIR_CMD:
            self.chdir(args)
        elif args[0] == LISTF_CMD:
            self.list_files(args)
        elif args[0] == LISTD_CMD:
            self.list_dirs(args)
        elif args[0] == SHOWLOG_CMD:
            self.print_log(args)
        elif args[0] == UNLOCK_PASSWD_CMD:
            self.unlock_passwd(args)
        else:
            self.logerr("Error: unknown command/program '{0}'".format(args[0]))
        return True

    def prompt(self):
        return PROMPT_BASE.format(pwd=self.curr_node.directory.name)

