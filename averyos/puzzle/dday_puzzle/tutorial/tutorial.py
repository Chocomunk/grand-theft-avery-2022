import sys

from shell.env import ENV

from gui.plotter import MeshPlotter
from system.filesystem import File, Node
from system.usrbin_programs import Chdir, Chdirid, ReadFile, Render, ListNode, \
                                    UnlockPassword, Help, ChdirBack

from .tutorial_files import *


class SheeshProg:
    NAME = "`sheesh`"
    DESC = ChdirBack.DESC


# TODO: Add fake files/dirs
def build_start():
    root = Node("tutorial-root")
    n1 = Node("Documents", parents=[root])

    # Back nav
    n1.add_child(root)

    # Programs
    read_prog = ReadFile()
    root.directory.add_program(read_prog.NAME, read_prog)

    ENV.visible_progs.add(Help)
    ENV.visible_progs.add(ReadFile)
    ENV.visible_progs.add(ListNode)

    # Files
    root.directory.add_file(security)
    n1.directory.add_file(doc_notes)

    # Callbacks
    n1.add_entry_callback(lambda _: ENV.visible_progs.add(Chdir))

    return [root, n1]


def build_documents(start_node):
    n2 = Node("institution-files", parents=[start_node])
    n3 = Node("avery-files", parents=[start_node])
    n4 =Node("misc", parents=[start_node])

    # Back nav
    n3.add_child(start_node)
    n4.add_child(start_node)

    # Files
    n3.directory.add_file(avery_desc1)
    n3.directory.add_file(avery_desc2)

    return [n2,n3,n4]


EXIT_NAME = "safe-directory"
TRAP_NAME = lambda i: "trap-directory-{}".format(i)

def build_trap(entry_node: Node, num_exit=100, num_trap=7):
    sike = Node("nice-try")
    caught = Node("caught-you!", parents=[sike])
    exit_node = Node("Security-Check")

    # Add files
    caught.directory.add_file(caught_file)

    # Callbacks
    sike.add_entry_callback(lambda _: ENV.visible_progs.add(SheeshProg))

    # Setup trap callbacks:
    cdprog = Chdir()
    cdidprog = Chdirid()

    def sheesh_fail_cb(n: Node):
        """ A callback which prints the 'sheesh attempt' message """
        print("A good try, unfortunately it was too WEEEAK.", file=sys.stderr)

    def cdid_cb(i):
        """ A wrapper for `cdid` which navigates to the exit node """
        def _func(_: Node):
            cdidprog.cli_main(["", str(exit_node.id)])
            del ENV.node_history[-(i+1):]                   # Clear polluted history
        return _func

    def trap_cb(idx, to_end=False):
        """ 
        A wrapper for `cd` which navigates a full path to the sink nodes 'sike' 
        or 'caught'. Specifically, navigate INTO the `idx`'th node in the trap
        (so that node must be a child).
        """
        def _func(_: Node):
            exit_len = max(0, num_exit - idx)
            trap_len = min(7, num_exit+num_trap - idx)
            path = (EXIT_NAME+"/")*exit_len
            path += "/".join([TRAP_NAME(i) for i in range(num_trap-trap_len,num_trap)])
            path += "/{0}".format(sike.directory.name)
            if to_end:
                path += "/{0}".format(caught.directory.name)
            else:
                curr, path = path.split('/', 1)
                print("\nNavigated backwards to: '{0}'".format(curr))
                print("SIKE Pulling you into: '{0}'\n".format(path), file=sys.stderr)
            cdprog.cli_main(["", path])
        return _func

    # Build trap
    exit_start = Node(EXIT_NAME)
    curr = exit_start
    curr.add_entry_callback(cdid_cb(0))                     # Navigate to exit
    curr.password = "\n-norender-\n"
    for i in range(1, num_exit):
        curr = Node(EXIT_NAME, parents=[curr])
        curr.add_entry_callback(cdid_cb(i))                 # Navigate to exit
        curr.password = "\n-norender-\n"
    for i in range(num_trap):
        curr = Node(TRAP_NAME(i), parents=[curr])
        curr.add_entry_callback(trap_cb(num_exit+i))        # Fall into sink
        curr.password = "\n-norender-\n"
    
    # Connect trap to "sink" nodes
    entry_node.add_child(exit_start)
    curr.add_child(sike)

    # Trap callbacks
    sike.add_entry_callback(sheesh_fail_cb)                 # Fail message
    entry_node.add_entry_callback(trap_cb(0, True))         # Enter trap

    return [sike, caught, exit_node]


# TODO: Pic of dog named cat 
def build_security_question(n: Node):
    n1 = Node("Continue", parents=[n])

    n.directory.add_file(File("RIP.png", filepath="puzzle/dday_puzzle/tutorial/ripdog.png"))

    # Callbacks
    unlock = UnlockPassword()
    n.directory.add_program(unlock.NAME, unlock)
    n.add_entry_callback(lambda _: ENV.visible_progs.add(UnlockPassword))

    n1.set_password("Bofa")
    n1.prompt = "What is the name of your favorite animal?"

    return [n1]


def build_hidden(n: Node):
    n1 = Node("Avery", parents=[n], backnav_wall=True, hidden=True)

    render_prog = Render()
    n.directory.add_program(render_prog.NAME, render_prog)

    n1.directory.add_file(
        File("note.txt", "We strongly recommend you take advantage of your numbers and complete these puzzles in parallel"))

    # Callbacks
    n.add_entry_callback(lambda _: ENV.visible_progs.add(Render))

    n.directory.add_file(gameover)
    n1.directory.add_file(gameon)

    return [n1]


# TODO: Make files
def build_tutorial_graph():
    start_nodes = build_start()
    documents_nodes = build_documents(start_nodes[-1])
    trap_nodes = build_trap(documents_nodes[0])
    captcha_nodes = build_security_question(trap_nodes[-1])
    hidden_nodes = build_hidden(captcha_nodes[-1])

    pts = []
    H = 5
    W = 6
    h = 0
    for _ in range(len(start_nodes)):
        pts.append((0,h))
        h += H
    for i in range(-1,2):
        pts.append((W*i,h))
    h += H
    for i in range(2):
        pts.append((W*(i-0.5), h))
    h += H
    for i in range(3):
        pts.append((0,h))
        h += H

    nodes = start_nodes + documents_nodes + trap_nodes + captcha_nodes + hidden_nodes
    ids = [n.id for n in nodes]
    # ids = [n.id for n in nodes[-3:]]
    # pts = pts[-3:]

    return nodes, MeshPlotter(pts, ids), START_MSG
