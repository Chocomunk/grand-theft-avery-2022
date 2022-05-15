"""
An example puzzle design
"""
from shell.env import ENV
from gui.plotter import MeshPlotter
from system.filesystem import File, Node

from puzzle.util import load_points, make_graph, add_dir_files


DIR = "puzzle/dday_puzzle/ciphers"


# ---------------------------- Global Puzzle State ---------------------------- 
class CipherPuzzleState:
    """ Keeps track of global puzzle variables """
    c_trigger = False


# --------------------------- Puzzle Logic/Behavior --------------------------- 



# ---------------------------- Main (build puzzle) ---------------------------- 

def build_caesar_graph():
    A = Node("A")
    B1 = Node("B1", parents=[A])
    B2 = Node("B2", parents=[A])
    B3 = Node("B3", parents=[A])

    add_dir_files(A, DIR+"/caesar")

    B1.set_password("railfence")
    B2.set_password("scytale")
    B3.set_password("columnar")

    def caesar_locked(n: Node):
        return B1.passlocked or B2.passlocked or B3.passlocked

    return [A,B1,B2,B3], caesar_locked


def build_trans_graph(parents, lock_func):
    C = Node("C", parents=parents)
    D1 = Node("D1", parents=[C])
    D2 = Node("D2", parents=[C])
    D3 = Node("D3", parents=[C])

    add_dir_files(C, DIR+"/transposition")

    C.set_lock_func(lock_func)
    D1.set_password("integrity")
    D2.set_password("courage")
    D3.set_password("tenacity")

    def trans_locked(n: Node):
        return D1.passlocked or D2.passlocked or D3.passlocked

    return [C,D1,D2,D3], trans_locked


def build_sub_graph(parents, lock_func):
    E = Node("E", parents=parents)
    F1 = Node("F1", parents=[E])
    F2 = Node("F2", parents=[E])

    # TODO: add dir files

    E.set_lock_func(lock_func)
    # TODO: set passwords

    def sub_locked(n: Node):
        return F1.passlocked or F2.passlocked

    return [E,F1,F2], sub_locked


def build_poly_graph(parents, lock_func):
    G = Node("G", parents=parents)
    H1 = Node("H1", parents=[G])
    H2 = Node("H2", parents=[G])

    # TODO: add dir files

    G.set_lock_func(lock_func)
    # TODO: set passwords

    def poly_locked(n: Node):
        return H1.passlocked or H2.passlocked

    return [G,H1,H2], poly_locked


def build_pub_graph(parents, lock_func):
    I = Node("I", parents=parents)
    J1 = Node("J1", parents=[I])
    J2 = Node("J2", parents=[I])

    # TODO: add dir files

    I.set_lock_func(lock_func)
    # TODO: set passwords

    def pub_locked(n: Node):
        return J1.passlocked or J2.passlocked

    return [I,J1,J2], pub_locked


def build_cipher_graph():
    caesar_nodes, caesar_locked = build_caesar_graph()
    trans_nodes, trans_locked = build_trans_graph(caesar_nodes[1:], caesar_locked)
    sub_nodes, sub_locked = build_sub_graph(trans_nodes[1:], trans_locked)
    poly_nodes, poly_locked = build_sub_graph(sub_nodes[1:], sub_locked)
    pub_nodes, pub_locked = build_pub_graph(poly_nodes[1:], poly_locked)

    K = Node("K", parents=pub_nodes[1:])
    K.set_lock_func(pub_locked)

    # Generate mesh
    H = 4
    h = 0
    pts = []
    for _ in range(2):
        pts.append((0, h))
        h+=H
        pts.extend([(-10,h), (0,h), (10,h)])
        h+=H
    for _ in range(3):
        pts.append((0, h))
        h+=H
        pts.extend([(-5,h), (5,h)])
        h+=H
    pts.append((0,h))

    return caesar_nodes[0], MeshPlotter(pts, radius=50).transform(scale=30,angle=-30)
