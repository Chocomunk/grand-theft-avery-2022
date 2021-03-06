import sys

from shell.env import ENV
from .filesystem import Node, File
from .program import ExitCode, ProgramBase, CLIProgramBase
from .path_utils import path_subdirs, get_file

from gui.constants import Colors
from gui.render import RenderWidget
from gui.labelbox import LabelBoxWidget
from gui.password import PasswordWidget
from gui.view import SplitView, MainView
from gui.directory import DirectoryWidget
from gui.imageviewer import ImageViewerWidget


# TODO: Documentation


EXIT_CMD = "brexit"
CHDIR_CMD = "go"
CHDIRN_CMD = "cdn"
CHDIRID_CMD = "cdid"
CDBACK_CMD = "sh"
LIST_CMD = "pepelaugh"
READFILE_CMD = "yoink"
SHOWLOG_CMD = "showlog"
HISTORY_CMD = "history"
PASSWD_CMD = "boom"
RENDER_CMD = "yourmom"
HELP_CMD = "help"


# TODO: remove showlog
def usrbin_progs():
    return {
        EXIT_CMD: SendExit(hidden=True),
        CHDIR_CMD: Chdir(),
        CHDIRN_CMD: ChdirName(hidden=True),
        CHDIRID_CMD: Chdirid(hidden=True),
        CDBACK_CMD: ChdirBack(),
        LIST_CMD: ListNode(),
        READFILE_CMD: ReadFile(),
        # SHOWLOG_CMD: ShowLog(),
        HISTORY_CMD: ShowHistory(),
        PASSWD_CMD: UnlockPassword(),
        RENDER_CMD: Render(),
        HELP_CMD: Help()
    }


class SendExit(CLIProgramBase):

    NAME = EXIT_CMD

    def cli_main(self, args) -> ExitCode:
        return ExitCode.EXIT


class Chdir(CLIProgramBase):

    NAME = CHDIR_CMD
    DESC = "Change Directory. Navigates into child node paths. Cannot navigate backwards."

    def __init__(self, check_locked=True, hidden=False):
        super().__init__(hidden)
        self.check_locked = check_locked

    def cli_main(self, args) -> ExitCode:
        if len(args) != 2:
            print("Error: Must specify a directory to '{0}' into".format(CHDIR_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        path = path_subdirs(args[1], self.check_locked)

        if not path:
            return ExitCode.ERROR

        # chdir through the path
        new_node = path[-1]
        ENV.node_history.extend(path[:-1])
        ENV.visited_nodes.update(path)
        ENV.curr_node = new_node
        new_node.call_entry_callbacks()
        return ExitCode.OK


class ChdirName(CLIProgramBase):

    NAME = CHDIRN_CMD

    def cli_main(self, args) -> ExitCode:
        if len(args) != 2:
            print("Error: {0} takes exactly 1 argument!".format(CHDIRN_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        name = args[1]
        if name not in Node.name_to_node:
            print("Error: could not find node '{0}'".format(name), file=sys.stderr)
            return ExitCode.ERROR

        new_node = Node.name_to_node[name]

        # Ignore locks and just chdir to new_node
        ENV.node_history.append(ENV.curr_node)
        ENV.visited_nodes.add(new_node)
        ENV.curr_node = new_node
        new_node.call_entry_callbacks()
        return ExitCode.OK


class Chdirid(CLIProgramBase):

    NAME = CHDIRID_CMD

    def cli_main(self, args) -> ExitCode:
        if len(args) != 2:
            print("Error: {0} takes exactly 1 argument!".format(CHDIRID_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        try:
            node_id = int(args[1])
        except ValueError as e:
            print("Error: node id must be an integer, '{0}' is invalid.".format(
                args[1]), file=sys.stderr)
            return ExitCode.ERROR

        if node_id >= len(Node.id_to_node):
            print("Error: invalid node id '{0}'".format(args[1]), file=sys.stderr)
            return ExitCode.ERROR

        new_node = Node.id_to_node[node_id]

        # Ignore locks and just chdir to new_node
        ENV.node_history.append(ENV.curr_node)
        ENV.visited_nodes.add(new_node)
        ENV.curr_node = new_node
        new_node.call_entry_callbacks()
        return ExitCode.OK


class ChdirBack(CLIProgramBase):
    """ This program implements 'sheesh' back-navigating """

    NAME = CDBACK_CMD
    DESC = "Backwards Navigation. Every 'e' moves back by 1 directory. Will stop on BREAK nodes."

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

            print("SH\tDirectories")
            print("--\t-----------")
            i = 0
            for i in range(del_len):
                print("E\t{0}/".format(ENV.node_history[-i-1].directory.name))
                if ENV.node_history[-i-1].backnav_wall:
                    print("BREAK")
                    break
            print("SH")

            i += 1
            ENV.curr_node = ENV.node_history[-i]
            del ENV.node_history[-i:]
            ENV.curr_node.call_entry_callbacks()
        
        return ExitCode.OK


class Render(ProgramBase):

    NAME = RENDER_CMD
    DESC = "Displays the map of the explored filesystem."

    def cli_main(self, args) -> ExitCode:
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(RENDER_CMD), 
                  file=sys.stderr)
            return ExitCode.ERROR

        print("Map is only available in the GUI!", file=sys.stderr)

        return ExitCode.OK

    def gui_main(self, gui, args) -> ExitCode:
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(RENDER_CMD),
                  file=sys.stderr)
            return ExitCode.ERROR
        
        render_widg = RenderWidget(gui.size, gui.pop_view, nodes=Node.id_to_node)
        new_view = MainView(gui.size)
        new_view.add_widget(render_widg)
        gui.push_view("render", new_view)
    
        return ExitCode.OK


class ListNode(ProgramBase):

    NAME = LIST_CMD
    DESC = "Displays the directory view."

    # TODO: allow ls for subdirs
    def cli_main(self, args) -> ExitCode:
        if len(args) > 2:
            print("Error: {0} takes up to 1 arguments".format(LIST_CMD), 
                file=sys.stderr)
            return ExitCode.ERROR

        # Search subdirectories
        if len(args) > 1:
            path = path_subdirs(args[1])
            if not path:
                return ExitCode.ERROR
            node = path[-1]

        # Just use this node
        else:
            node = ENV.curr_node

        children = node.list_children()
        files = node.directory.list_files()
        progs = node.directory.list_programs()
        dirname = node.directory.name
        
        print("\nDirectory: {0}".format(dirname))

        STR_TMP = "{0:>12}    {1:<}"
        print(STR_TMP.format("Type", "Name"))
        print(STR_TMP.format("----", "----"))
        for child in children:
            print(STR_TMP.format("directory", child.directory.name))
        for file in files:
            print(STR_TMP.format("file", file))
        for prog in progs:
            print(STR_TMP.format("executable", prog))
        print()

        return ExitCode.OK

    def gui_main(self, gui, args) -> ExitCode:
        if len(args) == 1:
            if gui.viewtag != "nav":        # Set to nav view
                dir_widg = DirectoryWidget()
                new_view = SplitView(dir_widg, gui.terminal, gui.size, 
                                    weight=0.2, bg_color1=Colors.NAV_BACKGROUND)
                gui.push_view("nav", new_view)
            else:                               # Unset nav view
                gui.pop_view()
            return ExitCode.OK
        else:
            return self.cli_main(args)


class ReadFile(ProgramBase):

    NAME = READFILE_CMD
    DESC = "Open and view a file."

    def parse_file(self, args) -> File | None:
        if len(args) != 2:
            print("Error: Must specify a file to '{0}'".format(READFILE_CMD), 
                file=sys.stderr)
            return None

        return get_file(args[1])

    def cli_main(self, args) -> ExitCode:
        file = self.parse_file(args)
        if not file:
            return ExitCode.ERROR
        data = file.get_data()

        print(data)
        return ExitCode.OK

    def gui_main(self, gui, args) -> ExitCode:
        file = self.parse_file(args)
        if not file:
            return ExitCode.ERROR
            
        if file.is_image:
            data = file.filepath
            widget = ImageViewerWidget
        else:
            data = file.get_data()
            widget = LabelBoxWidget

        # Just replace right-pane, leave directory view in left-pane
        if gui.viewtag == "nav":
            def return_terminal():
                gui.view.widg2 = gui.terminal
            label_widg = widget(data, return_terminal)
            gui.view.widg2 = label_widg

        # Make a new view.
        else:
            label_widg = widget(data, lambda: gui.pop_view())
            new_view = MainView(gui.size)
            new_view.add_widget(label_widg)
            gui.push_view("viewfile", new_view)

        return ExitCode.OK


class ShowLog(CLIProgramBase):

    NAME = SHOWLOG_CMD
    
    def cli_main(self, args) -> ExitCode:
        if len(args) > 2:
            print("Error: {0} takes up to 1 argument".format(SHOWLOG_CMD), 
                  file=sys.stderr)
            return ExitCode.ERROR
        start_i = 0 if len(args) == 1 else args[1]
        print(ENV.log.get(start_i))
        return ExitCode.OK


class ShowHistory(CLIProgramBase):

    NAME = HISTORY_CMD

    def cli_main(self, args) -> ExitCode:
        if len(args) > 2:
            print("Error: {0} takes up to 1 argument".format(SHOWLOG_CMD), 
                  file=sys.stderr)
            return ExitCode.ERROR

        start_i = 0 
        if len(args) == 2:
            try:
                hist_len = int(args[1])
            except ValueError:
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

    NAME = PASSWD_CMD
    DESC = "Unlocks a directory."

    def check_node(self, args):
        if len(args) < 2:
            print("Error: must specify a directory.", file=sys.stderr)
            return None

        dirname = args[1]
        node = ENV.curr_node.find_neighbor(dirname)

        if not node:
            pwd = ENV.curr_node.directory.name
            print("Error: could not find {0} within {1}.".format(
                dirname, pwd), file=sys.stderr)
            return None

        if node.lockfunc(node):
            if node.passlocked:
                print("Error: directory {0} is both system-locked and password-locked\n\t(some other action is required first)".format(
                    dirname), file=sys.stderr)
            else:
                print("Error: directory {0} is locked by the system (some other action is required)".format(
                    dirname), file=sys.stderr)
            return None

        if not node.passlocked:
            print("Directory '{0}' is not locked".format(dirname), file=sys.stderr)
            return None

        return dirname, node

    def cli_main(self, args) -> ExitCode:
        out = self.check_node(args)
        if not out:
            return ExitCode.ERROR
        dirname, node = out

        if len(args) == 3:
            passwd = args[2]
        else:
            passwd = input("Enter password for '{0}': ".format(node.directory.name))

        if node.try_password(passwd):
            print("Success! '{0}' is unlocked.".format(dirname))
        else:
            print("Incorrect password for '{0}'".format(dirname), file=sys.stderr)
        return ExitCode.OK

    def gui_main(self, gui, args) -> ExitCode:
        out = self.check_node(args)
        if not out:
            return ExitCode.ERROR
        dirname, node = out

        def leave_window(passwd):
            if node.try_password(passwd):
                print("Success! {0} is unlocked.".format(dirname))
            gui.pop_view()
            
        passwd_widg = PasswordWidget(node.password, leave_window, node.prompt, 
                                    ignore_caps=node.ignore_caps)
        new_view = MainView(gui.size)
        new_view.add_widget(passwd_widg)
        gui.push_view("passwd", new_view)
        return ExitCode.OK

class Help(CLIProgramBase):

    NAME = HELP_CMD
    DESC = "Displays a description for each encountered command"

    def cli_main(self, args) -> ExitCode:
        if len(args) != 1:
            print("Error: {0} does not take any arguments".format(HELP_CMD), 
                  file=sys.stderr)
            return ExitCode.ERROR

        for prog in ENV.visible_progs:
            print("{0}:\t{1}".format(prog.NAME, prog.DESC))

        return ExitCode.OK
