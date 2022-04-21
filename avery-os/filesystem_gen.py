from shell import Shell
from filesystem import File, Node, SystemState


# Example filesystem with locks
def test_filesystem1():
    # Define callback functions
    # TODO: consider defining event/state objects to pass into callbacks
    # This function unlocks F when C is stepped on 
    def f_lock(n: Node, shell: Shell):
        locked = not SystemState.c_trigger
        shell.log("Checking func-lock on {0}... Locked: {1}".format(
            n.directory.name, locked))
        return locked
    
    # This function signals that C is stepped on 
    def c_trig(n: Node, shell: Shell):
        SystemState.c_trigger = True
        shell.log("Stepped on {0}!".format(n.directory.name))
        
    # Build FS graph
    root = Node(dirname="root")
    a = Node(parents=[root], dirname="A")
    b = Node(parents=[a], dirname="B")
    c = Node(parents=[root, b], dirname="C")
    d = Node(parents=[a], dirname="D")
    e = Node(parents=[a,b,c,d], dirname="E")
    f = Node(parents=[e], dirname="F")
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
    f.set_lock(f_lock)

    return root