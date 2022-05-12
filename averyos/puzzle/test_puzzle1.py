"""
An example puzzle design
"""
from system.program import CLIProgramBase
from system.filesystem import File, Directory, Node


# ---------------------------- Global Puzzle State ---------------------------- 
class PuzzleState:
    """ Keeps track of global puzzle variables """
    nodes = []

    c_trigger = False       # Should be set to True when we step on 'c'


# --------------------------- Puzzle Logic/Behavior --------------------------- 
# Example puzzle program
class CheckC(CLIProgramBase):

    name = "checkc"

    def cli_main(self, args):
        print("C triggered: {0}".format(PuzzleState.c_trigger))


def new_node(state, parents=[], dirname="New Folder", directory: Directory=None):
    """ Wraps Node creation for state manipulation """
    n = Node(parents=parents, dirname=dirname, directory=directory)
    print("Created Node {0} (id {1})".format(n.directory.name, n.id))
    state.nodes.append(n)
    return n


# ---------------------------- Main (build puzzle) ---------------------------- 
def test_puzzle1():
    # Define state tracker
    state = PuzzleState

    # Define callback functions
    # This function unlocks F when C is stepped on 
    def f_lock(n: Node):
        locked = not state.c_trigger
        print("Checking func-lock on {0}... Locked: {1}".format(n.directory.name, locked))
        return locked
    
    # This function signals that C is stepped on 
    def c_trig(n: Node):
        state.c_trigger = True
        print("Stepped on {0}!".format(n.directory.name))
        
    # Build FS graph
    root = new_node(state, dirname="root")
    a = new_node(state, parents=[root], dirname="A")
    b = new_node(state, parents=[a], dirname="B")
    c = new_node(state, parents=[root, b], dirname="C")
    d = new_node(state, parents=[a], dirname="D")
    e = new_node(state, parents=[a,b,c,d], dirname="E")
    f = new_node(state, parents=[e, d], dirname="F")
    c.add_child(root)
    d.add_child(root)

    # Add files
    shared = File("shared.txt", "shared text")
    a.directory.add_file(File("a.txt", "a text\nNext Line"))
    b.directory.add_file(File("b.txt", filepath="puzzle/b.txt"))
    c.directory.add_file(shared)
    c.directory.add_file(File("space-cat.png", filepath="puzzle/space-cat.png", is_image=True))
    d.directory.add_file(shared)
    f.directory.add_file(File("f.txt", "ooga\nbooga"))

    # Add programs
    root.directory.add_program(CheckC.name, CheckC())
    a.directory.add_program(CheckC.name, CheckC())

    # Set callbacks
    c.add_entry_callback(c_trig)

    # Set locks
    e.set_password("gugma")
    f.set_lock_func(f_lock)

    return root