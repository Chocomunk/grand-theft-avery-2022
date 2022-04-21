import shlex
import argparse

from filesystem import Node


# ENVs
PROMPT_BASE = "[{pwd}]> "

# TODO: Automate command-name -> resolving command/program

# OS Commands
EXIT_CMD = "exit"
CHDIR_CMD = "cd"
LISTF_CMD = "lsf"
LISTD_CMD = "lsd"


class Shell:

    def __init__(self, root: Node):
        self.root = root
        self.curr_node = root

    def chdir(self, args):
        if len(args) != 2:
            print("Error: {0} only accepts 1 argument!".format(CHDIR_CMD))
            return self.curr_node

        dirname = args[1]
        new_node = self.curr_node.navigate(dirname)

        if not new_node:
            pwd = self.curr_node.directory.name
            print("Error: no directory named {0} connected to {1}!".format(dirname, pwd))
            return self.curr_node
        return new_node

    def list_files(self, args):
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(LISTF_CMD))
            return
        print(self.curr_node.directory.list_dir())

    def list_dirs(self, args):
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(LISTD_CMD))
            return
        print(self.curr_node.list_children())

    def handle_input(self, inp):
        args = shlex.split(inp)
        
        # Parse commands
        if args[0] == EXIT_CMD:
            return False
        elif args[0] == CHDIR_CMD:
            self.curr_node = self.chdir(args)
        elif args[0] == LISTF_CMD:
            self.list_files(args)
        elif args[0] == LISTD_CMD:
            self.list_dirs(args)
        elif len(args) > 0:
            print("Error: unknown command/program '{0}'".format(args[0]))
        return True

    def prompt(self):
        return PROMPT_BASE.format(pwd=self.curr_node.directory.name)

