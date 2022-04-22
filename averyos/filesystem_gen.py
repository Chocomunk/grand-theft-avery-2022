from shell import Shell
from filesystem import File, Directory, Node


# NOTE: Seeing if I can keep all the state stuff in one place (here) and just
#       manipulate them using callbacks.
# TODO: add state trackers for puzzles that need them
class SystemState1:
    """ Keeps track of global system variables """
    nodes = []

    # EXAMPLE:
    c_trigger = False       # Should be set to True when we step on 'c'


def new_node(state, parents=[], dirname="New Folder", directory: Directory=None):
    """ Wraps Node creation for state manipulation """
    n = Node(parents=parents, dirname=dirname, directory=directory)
    # TODO: remove prints
    print("Created Node {0} (id {1})".format(n.directory.name, n.id))
    state.nodes.append(n)
    return n


# Example filesystem with locks
def test_filesystem1():
    # Define state tracker
    state = SystemState1

    # Define callback functions
    # TODO: consider defining event/state objects to pass into callbacks
    # This function unlocks F when C is stepped on 
    def f_lock(n: Node, shell: Shell):
        locked = not state.c_trigger
        shell.log("Checking func-lock on {0}... Locked: {1}".format(
            n.directory.name, locked))
        return locked
    
    # This function signals that C is stepped on 
    def c_trig(n: Node, shell: Shell):
        state.c_trigger = True
        shell.log("Stepped on {0}!".format(n.directory.name))
        
    # Build FS graph
    root = new_node(state, dirname="root")
    a = new_node(state, parents=[root], dirname="A")
    b = new_node(state, parents=[a], dirname="B")
    c = new_node(state, parents=[root, b], dirname="C")
    d = new_node(state, parents=[a], dirname="D")
    e = new_node(state, parents=[a,b,c,d], dirname="E")
    f = new_node(state, parents=[e], dirname="F")
    c.add_child(root)
    d.add_child(root)

    # Add files
    shared = File("shared.txt", "shared text")
    a.directory.add_file(File("a.txt", "a text"))
    c.directory.add_file(shared)
    d.directory.add_file(shared)

    # Set callbacks
    c.add_entry_callback(c_trig)

    # Set locks
    e.set_password("gugma")
    f.set_lock_func(f_lock)

    return root