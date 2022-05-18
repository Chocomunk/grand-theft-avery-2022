from shell.env import ENV
from system.filesystem import Node
from gui.plotter import MeshPlotter
from .ciphers.ciphers import build_cipher_graph
from.wordplay.wordplay import build_emoji_graph
from system.usrbin_programs import usrbin_progs


def build_graph():
    # Setup ENV
    ENV.reset()
    ENV.path = usrbin_progs()

    # Build graph
    root = Node("root")

    cipher_nodes, cipher_mesh = build_cipher_graph()
    word_nodes, word_mesh = build_emoji_graph()

    root.add_child(cipher_nodes[0])
    root.add_child(word_nodes[0])

    # Combine meshes
    mesh = MeshPlotter([(0,0)],[root.id],radius=75)
    cipher_mesh = cipher_mesh.transform(scale=50, shift=(1000,100), angle=30)
    word_mesh = word_mesh.transform(scale=50, shift=(-1000,100), angle=-30)
    mesh.extend(cipher_mesh).extend(word_mesh)
    ENV.plotter = mesh
    
    return root, "AveryOS (TODO - UPDATE)"
