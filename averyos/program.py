import sys

from enum import Enum
from abc import ABC, abstractmethod

from shell import ENV


# -------------------- Define Programs --------------------


class ExitCode(Enum):
    OK = 0
    ERROR = 1
    EXIT = -1


class ProgramBase(ABC):

    @abstractmethod
    def cli_main(self, args) -> ExitCode:
        pass

    @abstractmethod
    def gui_main(self, args) -> ExitCode:
        pass


class CLIProgramBase(ProgramBase):

    @abstractmethod
    def cli_main(self, args) -> ExitCode:
        pass

    # GUI interface is just the text intergface
    def gui_main(self, args):
        return self.cli_main()


# -------------------- Default programs (usr/bin/) --------------------

EXIT_CMD = "exit"
CHDIR_CMD = "cd"
LISTF_CMD = "lsf"
LISTD_CMD = "lsd"
SHOWLOG_CMD = "showlog"
UNLOCK_PASSWD_CMD = "passwd"


def usrbin_progs():
    return {
        EXIT_CMD: SendExit(),
        CHDIR_CMD: Chdir(),
        LISTF_CMD: ListDirs(),
        LISTD_CMD: ListDirs(),
        SHOWLOG_CMD: ShowLog(),
        UNLOCK_PASSWD_CMD: UnlockPassword()
    }


class SendExit(CLIProgramBase):

    def cli_main(self, args):
        return ExitCode.EXIT


class Chdir(CLIProgramBase):

    def cli_main(self, args):
        if len(args) != 2:
            print("Error: {0} only accepts 1 argument!".format(CHDIR_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        dirname = args[1]
        new_node = ENV.curr_node.find_neighbor(dirname)

        if not new_node:
            pwd = ENV.curr_node.directory.name
            print("Error: no directory named {0} connected to {1}!".format(
                dirname, pwd), file=sys.stderr)
            return ExitCode.ERROR

        if not new_node.locked(new_node):
            ENV.curr_node = new_node
            new_node.call_entry_callbacks(new_node)
        else:
            print("Error: {0} is locked!".format(dirname))
            return ExitCode.ERROR
        return ExitCode.OK


class ListFiles(CLIProgramBase):

    def cli_main(self, args):
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(LISTF_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR
        print(ENV.curr_node.directory.list_dir())
        return ExitCode.OK


class ListDirs(CLIProgramBase):

    def cli_main(args):
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(LISTD_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR
        print(ENV.curr_node.list_children())
        return ExitCode.OK


class ShowLog(CLIProgramBase):
    
    def cli_main(args):
        if len(args) > 2:
            print("Error: {0} takes up to 1 argument".format(SHOWLOG_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR
        start_i = 0 if len(args) == 1 else args[1]
        print(ENV.log.get(start_i))
        return ExitCode.OK


class UnlockPassword(ProgramBase):

    def cli_main(self, args):
        if len(args) != 3:
            print("Error: {0} must take 2 arguments!".format(args[0]), 
                file=sys.stderr)
            return ExitCode.ERROR

        dirname = args[1]
        new_node = ENV.curr_node.find_neighbor(dirname)

        if not new_node:
            pwd = ENV.curr_node.directory.name
            print("Error: no directory named {0} connected to {1}!".format(
                dirname, pwd), file=sys.stderr)
            return ExitCode.ERROR
        
        if not new_node.passlocked:
            print("Error: directory {0} is not password-locked (something else?)".format(
                dirname), file=sys.stderr)
            return ExitCode.ERROR

        if new_node.try_password(args[2]):
            print("Success! {0} is unlocked.".format(dirname))
        else:
            print("Incorrect password for {0}".format(dirname), file=sys.stderr)
        return ExitCode.OK

    # TODO: create proper unlock GUI
    def gui_main(self, args):
        return self.cli_main(args)

