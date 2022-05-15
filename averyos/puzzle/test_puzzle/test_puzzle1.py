"""
An example puzzle design
"""
from shell.env import ENV
from gui.plotter import MeshPlotter
from system.program import CLIProgramBase
from system.filesystem import File, Node

from puzzle.util import load_points, make_graph, add_dir_files


# ---------------------------- Global Puzzle State ---------------------------- 
class PuzzleState:
    """ Keeps track of global puzzle variables """
    c_trigger = False       # Should be set to True when we step on 'c'


# --------------------------- Puzzle Logic/Behavior --------------------------- 
# Example puzzle program
class CheckC(CLIProgramBase):

    name = "checkc"

    def cli_main(self, args):
        print("C triggered: {0}".format(PuzzleState.c_trigger))


dirnames = ["root", "A", "B", "C", "D", "E", "F"]

# (row, col) -> (parent, child)
adj_mat = [
    [0, 1, 0, 1, 0, 0, 0],      # root
    [0, 0, 1, 0, 1, 1, 0],      # A
    [0, 0, 0, 1, 0, 1, 0],      # B
    [1, 0, 0, 0, 0, 1, 0],      # C
    [1, 0, 0, 0, 0, 1, 1],      # D
    [0, 0, 0, 0, 0, 0, 1],      # E
    [0, 0, 0, 0, 0, 0, 0]       # F
]


# ---------------------------- Main (build puzzle) ---------------------------- 
def test_puzzle1():
    # Define state tracker
    state = PuzzleState

    pts = load_points("puzzle/test_puzzle/Example-Spiral-Mesh.csv")
    ENV.plotter = MeshPlotter(pts)
        
    # Build FS graph
    nodes = make_graph(dirnames, adj_mat)
    root, a, b, c, d, e, f = [nodes[name] for name in dirnames]

    # Add files
    shared = File("shared.txt", "shared text")
    a.directory.add_file(File("a.txt", "a text\nNext Line"))
    b.directory.add_file(File("b.txt", filepath="puzzle/test_puzzle/b.txt"))
    c.directory.add_file(shared)
    c.directory.add_file(File("space-cat.png", filepath="puzzle/test_puzzle/space-cat.png"))
    d.directory.add_file(shared)
    f.directory.add_file(File("f.txt", "ooga\nbooga"))

    # Add programs
    chkc = CheckC()
    root.directory.add_program(CheckC.name, chkc)
    a.directory.add_program(CheckC.name, chkc)

    # Define callback functions
    # This function unlocks F when C is stepped on 
    def f_lock(n: Node):
        locked = not state.c_trigger
        print("Checking func-lock on {0}... Locked: {1}".format(n.directory.name, locked))
        return locked
    
    # This function signals that C is stepped on 
    def c_trig(n: Node):
        state.c_trigger = True
        chkc.hidden = True
        print("Stepped on {0}!".format(n.directory.name))

    # Set callbacks
    c.add_entry_callback(c_trig)

    # Set locks
    e.set_password("gug ma")
    f.set_lock_func(f_lock)

    return root, "Welcome to the AveryOS Test Puzzle!"