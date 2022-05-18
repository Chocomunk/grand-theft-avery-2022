"""
An example puzzle design
"""
from shell.env import ENV
from gui.plotter import MeshPlotter
from system.filesystem import Node
from .programs.histogram import Histogram
from .programs.sub_password import UnlockSubPassword
from .programs.prompt_password import UnlockPromptPassword

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
    prompt_unlock = UnlockPromptPassword(hidden=True)
    C.directory.add_program(prompt_unlock.NAME, prompt_unlock)

    D1_prompt = "TTGNS RIATH IYNHA DGTOA CPRLH NELOI OTHNR MLNAO UGEQA FENSA IOGPI LMPIS UBEVN RSRS"
    D2_prompt = "TFIEP HFMXR EOATE FRGES AMERE CISNN UNOAT LGRLT TNCOO YEOBT OWNJH RICEE ADECS CEPTE TATSE ISSNS OOOOE NRFTS O"
    D3_prompt = "TAOTI LTMNM HLRON RIEGL EIFFG TPTFY QTABA OSHIU YCEBG OIR"

    D1.prompt = "\n".join(D1_prompt.split(" "))
    D2.prompt = "\n".join(D2_prompt.split(" "))
    D3.prompt = "\n".join(D3_prompt.split(" "))

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

    add_dir_files(E, DIR+"/substitution")
    sub_unlock = UnlockSubPassword(hidden=True)
    E.directory.add_program(sub_unlock.NAME, sub_unlock)

    E.set_lock_func(lock_func)
    F1.set_password("oeznmiujxywbkravtdcqhflsgp")
    F2.set_password("jrhtywxvfcundmzkqgpboaiesl")

    def sub_locked(n: Node):
        return F1.passlocked or F2.passlocked

    return [E,F1,F2], sub_locked


def build_poly_graph(parents, lock_func):
    G = Node("G", parents=parents)
    H1 = Node("H1", parents=[G])
    H2 = Node("H2", parents=[G])
    H3 = Node("H3", parents=[G])
    H4 = Node("H4", parents=[G])

    add_dir_files(G, DIR+"/polyalphabetic")
    prompt_unlock = UnlockPromptPassword(hidden=True)
    G.directory.add_program(prompt_unlock.NAME, prompt_unlock)

    H1.prompt = "ptucpcdzlywluvv zs wbt"
    H2.prompt = "tlicmmbcdhuzmf hliuu"
    H3.prompt = "z nz o mf hrddwz rtkg"
    H4.prompt = "y nz lmgyc"

    G.set_lock_func(lock_func)
    H1.set_password("averyprivatekey is two")
    H2.set_password("myprivatekey is three")
    H3.set_password("q is p is twenty nine")
    H4.set_password("g is eight")

    def poly_locked(n: Node):
        return H1.passlocked or H2.passlocked or H3.passlocked or H4.passlocked

    return [G,H1,H2,H3,H4], poly_locked


def build_pub_graph(parents, lock_func):
    I = Node("I", parents=parents)
    J1 = Node("J1", parents=[I])
    J2 = Node("J2", parents=[I])

    add_dir_files(I, DIR+"/publickey")

    I.set_lock_func(lock_func)
    # TODO: set passwords

    def pub_locked(n: Node):
        return J1.passlocked or J2.passlocked

    return [I,J1,J2], pub_locked


# TODO: exit node


def build_cipher_graph():
    caesar_nodes, caesar_locked = build_caesar_graph()
    trans_nodes, trans_locked = build_trans_graph(caesar_nodes[1:], caesar_locked)
    sub_nodes, sub_locked = build_sub_graph(trans_nodes[1:], trans_locked)
    poly_nodes, poly_locked = build_poly_graph(sub_nodes[1:], sub_locked)
    pub_nodes, pub_locked = build_pub_graph(poly_nodes[1:], poly_locked)

    K = Node("K", parents=pub_nodes[1:])
    K.set_lock_func(pub_locked)

    # Generate mesh
    H = 5
    h = 0
    pts = []
    for _ in range(2):
        pts.append((0, h))
        h+=H
        pts.extend([(-7,h), (0,h), (7,h)])
        h+=H
    for _ in range(3):
        pts.append((0, h))
        h+=H
        pts.extend([(-5,h), (5,h)])
        h+=H
    pts.append((0,h))

    nodes = caesar_nodes + trans_nodes + sub_nodes + poly_nodes + pub_nodes
    ids = [n.id for n in nodes]

    hist_prog = Histogram()
    ENV.path[hist_prog.NAME] = hist_prog

    return nodes, MeshPlotter(pts, ids)
