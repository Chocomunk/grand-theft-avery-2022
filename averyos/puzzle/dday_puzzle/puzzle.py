from shell.env import ENV

from system.filesystem import Node
from system.usrbin_programs import usrbin_progs

from gui.plotter import MeshPlotter

from .ciphers.ciphers import build_cipher_graph
from .wordplay.wordplay import build_emoji_graph
from .tutorial.tutorial import build_tutorial_graph
from .fanfic.fanfic import build_fanfic_graph


def build_graph():
    # Setup ENV
    ENV.reset()
    ENV.path = usrbin_progs()

    # Build graph
    start_msg = "AveryOs (TODO)"
    tutorial_nodes, tutorial_mesh, start_msg = build_tutorial_graph()
    # cipher_nodes, cipher_mesh = build_cipher_graph()
    word_nodes, word_mesh = build_emoji_graph()
    fanfic_nodes, fanfic_mesh = build_fanfic_graph()

    root = tutorial_nodes[0]
    start = tutorial_nodes[-1]
    # start.add_child(cipher_nodes[0])
    start.add_child(word_nodes[0])
    start.add_child(fanfic_nodes[0])
    # root = word_nodes[0]

    # Combine meshes
    mesh = MeshPlotter([],[],radius=75)

    tutorial_mesh = tutorial_mesh.transform(scale=50, shift=(0,-1900))
    # cipher_mesh = cipher_mesh.transform(scale=50, shift=(300,0), angle=60)
    word_mesh = word_mesh.transform(scale=50, shift=(-300,0), angle=-60)
    # TODO: fanfic mesh

    mesh.extend(tutorial_mesh)
    # mesh.extend(cipher_mesh)
    mesh.extend(word_mesh)

    ENV.plotter = mesh
    
    return root, start_msg
