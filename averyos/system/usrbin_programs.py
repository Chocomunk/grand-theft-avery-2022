import sys

from shell.env import ENV
from .filesystem import Node
from .program import ExitCode, ProgramBase, CLIProgramBase


EXIT_CMD = "exit"
CHDIR_CMD = "cd"
CHDIRID_CMD = "cdid"
CDBACK_CMD = "sh"
LIST_CMD = "ls"
SHOWLOG_CMD = "showlog"
HISTORY_CMD = "history"
PASSWD_CMD = "passwd"


def usrbin_progs():
    return {
        EXIT_CMD: SendExit(),
        CHDIR_CMD: Chdir(),
        CHDIRID_CMD: Chdirid(),
        CDBACK_CMD: ChdirBack(),
        LIST_CMD: ListNode(),
        SHOWLOG_CMD: ShowLog(),
        HISTORY_CMD: ShowHistory(),
        PASSWD_CMD: UnlockPassword()
    }


class SendExit(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
        return ExitCode.EXIT


class Chdir(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
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

        if not new_node.locked():
            ENV.node_history.append(ENV.curr_node)
            ENV.curr_node = new_node
            new_node.call_entry_callbacks()
        else:
            print("Error: {0} is locked!".format(dirname))
            return ExitCode.ERROR
        return ExitCode.OK


class Chdirid(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
        if len(args) != 2:
            print("Error: {0} only accepts 1 argument!".format(CHDIRID_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        try:
            node_id = int(args[1])
        except ValueError as e:
            print("Error: node id must be an integer, {0} is invalid.".format(
                args[1]), file=sys.stderr)
            return ExitCode.ERROR

        if node_id >= len(Node.id_to_node):
            print("Error: invalid node id {0}".format(args[1]), file=sys.stderr)
            return ExitCode.ERROR

        new_node = Node.id_to_node[node_id]

        # Ignore locks and just chdir to new_node
        ENV.node_history.append(ENV.curr_node)
        ENV.curr_node = new_node
        new_node.call_entry_callbacks()
        return ExitCode.OK


class ChdirBack(CLIProgramBase):
    """ This program implements 'sheesh' back-navigating """

    def cli_main(self, args) -> ExitCode:
        if len(args) != 2:
            print("Error: caller has a weak 'sheesh'", file=sys.stderr)
            return ExitCode.ERROR

        argl = len(args[1])
        len_e = argl if argl < 2 else argl - 2
        es = args[1][:len_e]            # Substring of only the e's
        if es != len_e * 'e':
            print("Error: wtf is 'sh{0}'??????".format(args[1]), 
                file=sys.stderr)
            return ExitCode.ERROR

        if not args[1].endswith("sh"):
            print("Error: didn't end the 'sheesh' smh", file=sys.stderr)
            return ExitCode.ERROR

        if len_e == 0:
            print("(shsh... don't move...)")
        else:
            hist_len = len(ENV.node_history)
            del_len = min(len_e, hist_len)

            if del_len == 0: 
                print("No space to 'sheesh'. This is so sad...")
                return ExitCode.OK

            print("SH")
            for i in range(del_len):
                print("E\t{0}".format(ENV.node_history[-i-1].directory.name))
            print("SH")

            ENV.curr_node = ENV.node_history[-del_len]
            del ENV.node_history[-del_len:]
        
        return ExitCode.OK


class ListNode(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(LIST_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        files = ENV.curr_node.directory.list_files()
        progs = ENV.curr_node.directory.list_programs()
        dirs = ENV.curr_node.list_children()
        cwd = ENV.curr_node.directory.name
        
        print("\nDirectory: {0}".format(cwd))

        STR_TMP = "{0:>12}\t{1:<}"
        print(STR_TMP.format("Type", "Name"))
        print(STR_TMP.format("----", "----"))
        for dir in dirs:
            print(STR_TMP.format("directory", dir))
        for prog in progs:
            print(STR_TMP.format("executable", prog))
        for file in files:
            print(STR_TMP.format("file", file))
        print()

        return ExitCode.OK


class ShowLog(CLIProgramBase):
    
    def cli_main(self, args) -> ExitCode:
        if len(args) > 2:
            print("Error: {0} takes up to 1 argument".format(SHOWLOG_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR
        start_i = 0 if len(args) == 1 else args[1]
        print(ENV.log.get(start_i))
        return ExitCode.OK


class ShowHistory(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
        if len(args) > 2:
            print("Error: {0} takes up to 1 argument".format(SHOWLOG_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        start_i = 0 
        if len(args) == 2:
            try:
                hist_len = int(args[1])
            except ValueError as e:
                print("Error: '{0}' is not an integer".format(args[1]), 
                    file=sys.stderr)
                return ExitCode.ERROR
            start_i = max(0, len(ENV.node_history) - hist_len)

        print([n.directory.name for n in ENV.node_history[start_i:]])
        return ExitCode.OK


class UnlockPassword(ProgramBase):

    def cli_main(self, args) -> ExitCode:
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
    def gui_main(self, args) -> ExitCode:
        return self.cli_main(args)
