import re
import sys

from shell.env import ENV
from .filesystem import Node
from .program import ExitCode, ProgramBase, CLIProgramBase

from gui.view import SplitView, MainView
from gui.directory import DirectoryWidget
from gui.labelbox import LabelBoxWidget
from gui.password import PasswordWidget


EXIT_CMD = "exit"
CHDIR_CMD = "cd"
CHDIRID_CMD = "cdid"
CDBACK_CMD = "sh"
LIST_CMD = "ls"
READFILE_CMD = "cat"
SHOWLOG_CMD = "showlog"
HISTORY_CMD = "history"
PASSWD_CMD = "unlock"


# TODO: remove showlog
def usrbin_progs():
    return {
        EXIT_CMD: SendExit(),
        CHDIR_CMD: Chdir(),
        CHDIRID_CMD: Chdirid(),
        CDBACK_CMD: ChdirBack(),
        LIST_CMD: ListNode(),
        READFILE_CMD: ReadFile(),
        # SHOWLOG_CMD: ShowLog(),
        HISTORY_CMD: ShowHistory(),
        PASSWD_CMD: UnlockPassword()
    }


class SendExit(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
        return ExitCode.EXIT


def clean_path(s):
    return re.sub('//+', '/', s).strip('/')


class Chdir(CLIProgramBase):

    def cli_main(self, args) -> ExitCode:
        if len(args) != 2:
            print("Error: {0} only accepts 1 argument!".format(CHDIR_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        dirname = clean_path(args[1])
        path = ENV.curr_node.find_node(dirname)

        if not path:
            pwd = ENV.curr_node.directory.name
            print("Error: could not find {0} under {1}".format(
                dirname, pwd), file=sys.stderr)
            return ExitCode.ERROR

        new_node = path[-1]
        if not new_node.locked():
            ENV.node_history.extend(path[:-1])
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


class ListNode(ProgramBase):

    # TODO: allow ls for subdirs
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

        STR_TMP = "{0:>12}    {1:<}"
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

    def gui_main(self, gui, args) -> ExitCode:
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(LIST_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR
            
        if gui.viewtag != "nav":        # Set to nav view
            dir_widg = DirectoryWidget()
            new_view = SplitView(dir_widg, gui.terminal, gui.size, 
                                weight=0.2, bg_color1=(50,50,50))
            gui.push_view("nav", new_view)
        else:                               # Unset nav view
            gui.pop_view()
        return ExitCode.OK


class ReadFile(ProgramBase):

    def get_file_data(self, args):
        if len(args) != 2:
            print("Error: {0} only accepts 1 argument!".format(READFILE_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR, None
        pwd = ENV.curr_node.directory.name

        split = clean_path(args[1]).rsplit('/', 1)
        filename = split[-1]                # Last entry is filename

        cont_node = ENV.curr_node           # Default search in curr_node
        if len(split) > 1:
            dirname = split[0]
            path = ENV.curr_node.find_node(dirname)

            if not path:
                print("Error: could not find {0} under {1}".format(
                    dirname, pwd), file=sys.stderr)
                return ExitCode.ERROR, None
            cont_node = path[-1]            # Search under final node in path

        if filename not in cont_node.directory.files:
            print("Error: no file named {0} under {1}".format(
                filename, pwd), file=sys.stderr)
            return ExitCode.ERROR, None

        return ExitCode.OK, cont_node.directory.files[filename].data

    def cli_main(self, args) -> ExitCode:
        print(self.get_file_data(args))

        return ExitCode.OK

    def gui_main(self, gui, args) -> ExitCode:
        data = self.get_file_data(args)
            
        # Just replace right-pane, leave directory view in left-pane
        if gui.viewtag == "nav":
            def return_terminal():
                gui.view.widg2 = gui.terminal
            label_widg = LabelBoxWidget(data, return_terminal)
            gui.view.widg2 = label_widg

        # Make a new view.
        else:
            label_widg = LabelBoxWidget(data, lambda: gui.pop_view())
            new_view = MainView(gui.size)
            new_view.add_widget(label_widg)
            gui.push_view("viewfile", new_view)
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

        hist = [n.directory.name for n in ENV.node_history[start_i:]]
        chain_str = " -> ".join(hist)
        chain_str += " :=> {0}".format(ENV.curr_node.directory.name)
        print(chain_str)
        return ExitCode.OK


class UnlockPassword(ProgramBase):

    def check_node(self, args):
        if len(args) < 2:
            print("Error: must specify a directory.", file=sys.stderr)
            return ExitCode.ERROR, None

        dirname = args[1]
        new_node = ENV.curr_node.find_neighbor(dirname)

        if not new_node:
            pwd = ENV.curr_node.directory.name
            print("Error: could not find {0} within {1}.".format(
                dirname, pwd), file=sys.stderr)
            return ExitCode.ERROR, None

        return ExitCode.OK, (dirname, new_node)

    def cli_main(self, args) -> ExitCode:
        status, out = self.check_node(args)
        if status != ExitCode.OK:
            return status
        dirname, new_node = out
        
        if not new_node.passlocked:
            print("Error: directory {0} is not password-locked (something else?)".format(
                dirname), file=sys.stderr)
            return ExitCode.ERROR

        if len(args) == 3:
            passwd = args[2]
        else:
            passwd = input("Enter password for {0}: ".format(new_node.directory.name))

        if new_node.try_password(passwd):
            print("Success! {0} is unlocked.".format(dirname))
        else:
            print("Incorrect password for {0}".format(dirname), file=sys.stderr)
        return ExitCode.OK

    # TODO: create proper unlock GUI
    def gui_main(self, gui, args) -> ExitCode:
        status, out = self.check_node(args)
        if status != ExitCode.OK:
            return status
        _, new_node = out
            
        passwd_widg = PasswordWidget(new_node.password, lambda: gui.pop_view())
        new_view = MainView(gui.size)
        new_view.add_widget(passwd_widg)
        gui.push_view("passwd", new_view)
        passwd_widg.active = True
        return ExitCode.OK
