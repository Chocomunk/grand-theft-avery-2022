from hashlib import new
import shlex
import argparse

from filesystem import test_filesystem1


# ENVs
PROMPT_BASE = "[{pwd}]> "

# TODO: Automate command-name -> resolving command/program
# TODO: Organize code structure
# TODO: Consider program support

# OS Commands
EXIT_CMD = "exit"
CHDIR_CMD = "cd"
LISTF_CMD = "lsf"
LISTD_CMD = "lsd"


def chdir(args, curr_node):
    if len(args) != 2:
        print("Error: {0} only accepts 1 argument!".format(CHDIR_CMD))
        return curr_node

    dirname = args[1]
    new_node = curr_node.navigate(dirname)

    if not new_node:
        pwd = curr_node.directory.name
        print("Error: no directory named {0} connected to {1}!".format(dirname, pwd))
        return curr_node
    return new_node


def list_files(args, curr_node):
    if len(args) != 1:
        print("Error: {0} does not take any arguments".format(LISTF_CMD))
        return
    print(curr_node.directory.list_dir())


def list_dirs(args, curr_node):
    if len(args) != 1:
        print("Error: {0} does not take any arguments".format(LISTD_CMD))
        return
    print(curr_node.list_children())


def main():
    root = test_filesystem1()
    curr_node = root
    while True:
        pwd = curr_node.directory.name
        prompt = PROMPT_BASE.format(pwd=pwd)
        args = shlex.split(input(prompt))
        
        # Parse commands
        if len(args) == 0:      # Nothing entered
            continue
        elif args[0] == EXIT_CMD:
            break
        elif args[0] == CHDIR_CMD:
            curr_node = chdir(args, curr_node)
        elif args[0] == LISTF_CMD:
            list_files(args, curr_node)
        elif args[0] == LISTD_CMD:
            list_dirs(args, curr_node)
        else:
            print("Error: unknown command/program '{0}'".format(args[0]))


if __name__ == '__main__':
    main()

