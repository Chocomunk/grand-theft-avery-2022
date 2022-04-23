import sys 

from enum import Enum


class ExitCodes(Enum):
    OK = 0
    ERROR = 1
    EXIT = -1


# TODO: turn some of these into normal programs
# OS Commands
EXIT_CMD = "exit"
CHDIR_CMD = "cd"
LISTF_CMD = "lsf"
LISTD_CMD = "lsd"
SHOWLOG_CMD = "showlog"
UNLOCK_PASSWD_CMD = "passwd"


def send_exit(env, args):
    return ExitCodes.EXIT


def chdir(env, args):
    if len(args) != 2:
        print("Error: {0} only accepts 1 argument!".format(CHDIR_CMD), file=sys.stderr)
        return ExitCodes.ERROR

    dirname = args[1]
    new_node = env.curr_node.find_neighbor(dirname)

    if not new_node:
        pwd = env.curr_node.directory.name
        print("Error: no directory named {0} connected to {1}!".format(dirname, pwd), file=sys.stderr)
        return ExitCodes.ERROR

    if not new_node.locked(new_node):
        env.curr_node = new_node
        new_node.call_entry_callbacks(new_node)
    else:
        print("Error: {0} is locked!".format(dirname))
        return ExitCodes.ERROR
    return ExitCodes.OK


def unlock_passwd(env, args):
    if len(args) != 3:
        print("Error: {0} must take 2 arguments!".format(UNLOCK_PASSWD_CMD), file=sys.stderr)
        return ExitCodes.ERROR

    dirname = args[1]
    new_node = env.curr_node.find_neighbor(dirname)

    if not new_node:
        pwd = env.curr_node.directory.name
        print("Error: no directory named {0} connected to {1}!".format(dirname, pwd), file=sys.stderr)
        return ExitCodes.ERROR
    
    if not new_node.passlocked:
        print("Error: directory {0} is not password-locked (something else?)".format(dirname), file=sys.stderr)
        return ExitCodes.ERROR

    if new_node.try_password(args[2]):
        print("Success! {0} is unlocked.".format(dirname))
    else:
        print("Incorrect password for {0}".format(dirname), file=sys.stderr)
    return ExitCodes.OK


def list_files(env, args):
    if len(args) != 1:
        print("Error: {0} does not take any arguments".format(LISTF_CMD), file=sys.stderr)
        return ExitCodes.ERROR
    print(env.curr_node.directory.list_dir())
    return ExitCodes.OK


def list_dirs(env, args):
    if len(args) != 1:
        print("Error: {0} does not take any arguments".format(LISTD_CMD), file=sys.stderr)
        return ExitCodes.ERROR
    print(env.curr_node.list_children())
    return ExitCodes.OK


def print_log(env, args):
    if len(args) > 2:
        print("Error: {0} takes up to 1 argument".format(SHOWLOG_CMD), file=sys.stderr)
        return ExitCodes.ERROR
    start_i = 0 if len(args) == 1 else args[1]
    print(env.log.get(start_i))
    return ExitCodes.OK


SYSPROG_MAP = {
    EXIT_CMD: send_exit,
    CHDIR_CMD: chdir,
    LISTF_CMD: list_files,
    LISTD_CMD: list_dirs,
    SHOWLOG_CMD: print_log,
    UNLOCK_PASSWD_CMD: unlock_passwd
}
