import sys

from shell.env import ENV
from puzzle.util import add_dir_files

from gui.plotter import MeshPlotter
from system.filesystem import File, Node
from system.usrbin_programs import Chdir, Chdirid, ReadFile, Render, ListNode

from puzzle.dday_puzzle.programs.prompt_password import UnlockPromptPassword


START_MSG = \
"""
Welcome to AveryOS!

There will be some kind of hint in the room or here or smth to tell the user to type:
    > ls
Maybe also have a "locked" screen that they need a password for?
(entertaining shell message)
"""


# TODO: Add fake files/dirs
def build_start():
    root = Node("root (tutorial)")
    n1 = Node("Documents", parents=[root])
    n2 = Node("institution-files", parents=[n1])

    # Back nav
    n1.add_child(root)
    n2.add_child(n1)

    # Programs
    read_prog = ReadFile()
    root.directory.add_program(read_prog.NAME, read_prog)

    ENV.visible_progs.add(ReadFile.NAME)
    ENV.visible_progs.add(ListNode.NAME)

    # Files
    root.directory.add_file(File("OntoMe?.txt", 
        data="(WIP) {I changed the command names for security!} use 'cd' to navigate!"))
    n1.directory.add_file(File("some-doc.txt", "some text"))

    # Callbacks
    n1.add_entry_callback(lambda _: ENV.visible_progs.add(Chdir.NAME))

    return [root, n1, n2]


# TODO: Better names
# TODO: better sheesh hint
# TODO: better "strong" pun
EXIT_NAME = "safe-directory"
TRAP_NAME = lambda i: "trap-directory-{}".format(i)

def build_trap(entry_node: Node, num_exit=100, num_trap=7):
    sike = Node("Get rolled omegalul")
    caught = Node("Caught you!", parents=[sike])
    exit_node = Node("Security Check")

    # Add files
    caught.directory.add_file(File("goodfilename.txt", data="(some hint). Type 'sheesh'"))

    # Callbacks
    sike.add_entry_callback(lambda _: ENV.visible_progs.add("`sheesh`"))

    # Setup trap callbacks:
    cdprog = Chdir()
    cdidprog = Chdirid()

    def sheesh_fail_cb(n: Node):
        """ A callback which prints the 'sheesh attempt' message """
        print("A good try, unfortunately it was too WEAK.", file=sys.stderr)

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
                print("\nLanded on: '{0}'".format(curr))
                print("Navigating back to: '{0}'\n".format(path), file=sys.stderr)
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
    prompt_unlock = UnlockPromptPassword()
    n.directory.add_program(prompt_unlock.NAME, prompt_unlock)

    # Callbacks
    n.add_entry_callback(lambda _: ENV.visible_progs.add(prompt_unlock.NAME))

    n1.set_password("Bofa")
    n1.prompt = "What is the name of your favorite animal?"

    return [n1]


def build_hidden(n: Node):
    n1 = Node("Avery", parents=[n], backnav_wall=True, hidden=True)

    render_prog = Render()
    n.directory.add_program(render_prog.NAME, render_prog)

    # Callbacks
    n.add_entry_callback(lambda _: ENV.visible_progs.add(Render.NAME))

    n.directory.add_file(File("gameover.txt", 
        "You hackers are annoying! The only way to get past this one is hidden in my office. Good luck getting inside!"))
    n1.directory.add_file(File("game-is-on.txt",
        "Looks like an institution spy broke into my office... Now the real game is on!\nI've secured everything I have, good luck getting through!"))

    return [n1]


# TODO: Make files
def build_tutorial_graph():
    start_nodes = build_start()
    trap_nodes = build_trap(start_nodes[-1])
    captcha_nodes = build_security_question(trap_nodes[-1])
    hidden_nodes = build_hidden(captcha_nodes[-1])

    nodes = start_nodes + trap_nodes + captcha_nodes + hidden_nodes
    mesh_pts = [(0, i*5) for i in range(len(nodes))]
    ids = [n.id for n in nodes]

    return nodes, MeshPlotter(mesh_pts, ids), START_MSG
