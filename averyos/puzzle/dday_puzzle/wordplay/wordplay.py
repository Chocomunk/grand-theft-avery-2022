from system.filesystem import File, Node
from gui.plotter import MeshPlotter
from puzzle.util import add_dir_files

from .wordplay_files import *


BASE_DIR = "puzzle/dday_puzzle/wordplay"

# TODO: add exit

def emoji_pts():
    H = 6
    W = 5

    h = 0
    pts = [(0,h)]
    h += H
    for i in range(-3,3):
        pts.append(((i+0.5)*W, h))
    h += H
    for i in range(-2,3):
        pts.append((i*W,h))
    h += H
    pts.append((-W,h))
    pts.append((W,h))
    pts.append((0,h+0.65*H))

    return pts


def build_emoji_graph():
    root = Node("emoji")

    n1 = Node("1", parents=[root])
    n2 = Node("2", parents=[root])
    n3 = Node("3", parents=[root])
    n4 = Node("4", parents=[root])
    n5 = Node("5", parents=[root])
    n6 = Node("6", parents=[root])

    n7 = Node("7", parents=[n1,n3])
    n8 = Node("8", parents=[n2,n3])
    n9 = Node("9", parents=[n3,n4])
    n10 = Node("10", parents=[n3,n5])
    n11 = Node("11", parents=[n5,n6])

    n12 = Node("12", parents=[n7,n8])
    n13 = Node("13", parents=[n9,n10])

    n14 = Node("14", parents=[n12,n13])

    nodes = [root, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14]

    # Files
    graph_pic = File("wordgraph.png", filepath=(BASE_DIR+"/files/wordgraph2.png"))
    for n in nodes:
        n.directory.add_file(graph_pic)
    root.directory.add_file(
        File("note.txt", "We highly recommend trying to do this puzzle in parallel."))
    root.directory.add_file(
        File("instructions.txt", 
"""
I secured this cluster of nodes by giving them interrelated passwords, then encrypting them with a caesar cipher. However,
I soon realized that it was way to hard to remember how to get through all that security. To make it easier to break the
security system I made, I added `wordgraph.png` to represent the nodes.

Each square is a single emoji, and each like space is a single word. The emojis not only help me figure out the words,
but also help me determine the encrypted password by putting them together applying my secret code.
"""))

    for f in ch1:
        n2.directory.add_file(f)
    for f in ch2:
        n3.directory.add_file(f)
    for f in ch3:
        n4.directory.add_file(f)
    for f in ch4:
        n6.directory.add_file(f)
    for f in ch5:
        n7.directory.add_file(f)
    for f in ch6:
        n9.directory.add_file(f)
    for f in ch7:
        n12.directory.add_file(f)

    # Passwords
    n2.set_password("Jwwbg")
    n3.set_password("Lsywi")
    n4.set_password("Dyhub")
    n6.set_password("Mpyl")

    n7.set_password("Psgh vcigs")
    n9.set_password("Idmzg pwcam")

    n12.set_password("Reejo xekiu yi jxu ruij xekiu")
    n13.set_password("Gbkxe nuayk oy g lotk nuayk")

    n14.set_password("Kfobi Ryeco sc Lyydi Ryeco")
    n14.prompt = "Red is greater than pink"

    # Locks
    n7.set_lock_func(lambda _: n1.passlocked or n3.passlocked)
    n9.set_lock_func(lambda _: n3.passlocked or n4.passlocked)
    n12.set_lock_func(lambda _: n7.passlocked or n8.passlocked)
    n13.set_lock_func(lambda _: n9.passlocked or n10.passlocked)
    n14.set_lock_func(lambda _: n12.passlocked or n13.passlocked)

    mesh_pts = emoji_pts()
    ids = [n.id for n in nodes]

    return nodes, MeshPlotter(mesh_pts, ids)


def emoji_pts_old():
    H = 6
    W = 5

    pts = [(0,0)]
    for i in range(1,3):
        for j in range(-2,3):
            pts.append((j*W, i*H))
    pts.append((-W,H*3))
    pts.append((W,H*3))

    return pts


def build_emoji_graph_old():
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
    root.directory.add_file(
        File("note.txt", "We highly recommend trying to do this puzzle in parallel."))

    lit_file = File("emoji_10.png", filepath=(BASE_DIR+"/emojis/lit_emoji.png"), hidden=True)
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
