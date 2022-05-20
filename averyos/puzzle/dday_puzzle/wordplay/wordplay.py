from system.filesystem import File, Node
from gui.plotter import MeshPlotter
from puzzle.util import add_dir_files


BASE_DIR = "puzzle/dday_puzzle/wordplay"

# TODO: add exit

def emoji_pts():
    H = 6
    W = 7

    pts = [(0,0)]
    for i in range(1,3):
        for j in range(-2,3):
            pts.append((j*W, i*H))
    pts.append((-W,H*3))
    pts.append((W,H*3))

    return pts


def build_emoji_graph():
    root = Node("emoji")

    n1 = Node("1", parents=[root])
    n2 = Node("2", parents=[root])
    n3 = Node("3", parents=[root])
    n4 = Node("4", parents=[root])
    n5 = Node("5", parents=[root])

    n6 = Node("6", parents=[n1,n2])
    n7 = Node("7", parents=[n2,n3])
    n8 = Node("8", parents=[n2,n4])
    n9 = Node("9", parents=[n2,n5])
    n10 = Node("10", parents=[n3,n5])

    n11 = Node("11", parents=[n6,n7])
    n12 = Node("12", parents=[n6,n10])

    nodes = [root, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12]

    # Files
    for n in nodes:
        add_dir_files(n, BASE_DIR+"/wordgraph")

    lit_file = File("emojis.png", filepath=(BASE_DIR+"/emojis/lit_emoji.png"), hidden=True)
    n3.directory.add_file(lit_file)
    n5.directory.add_file(lit_file)

    # Passwords
    n1.set_password("Booty")
    n2.set_password("House")
    n5.set_password("Fire")

    n7.set_password("Best house")
    n10.set_password("Its lit")

    n11.set_password("Booty house is best house")
    n12.set_password("Booty house is lit")

    # Locks
    n6.set_lock_func(lambda _: n1.passlocked or n2.passlocked)
    n7.set_lock_func(lambda _: n2.passlocked or n3.passlocked)
    n8.set_lock_func(lambda _: n2.passlocked or n4.passlocked)
    n9.set_lock_func(lambda _: n2.passlocked or n5.passlocked)
    n10.set_lock_func(lambda _: n3.passlocked or n5.passlocked)

    n11.set_lock_func(lambda _: n6.passlocked or n7.passlocked)
    n12.set_lock_func(lambda _: n6.passlocked or n10.passlocked)

    # Callbacks
    def _update_lit(_: Node):
        if not n3.locked() and not n5.locked():
            lit_file.hidden = False
    
    n3.add_entry_callback(_update_lit)
    n5.add_entry_callback(_update_lit)

    mesh_pts = emoji_pts()
    ids = [n.id for n in nodes]

    return nodes, MeshPlotter(mesh_pts, ids)
