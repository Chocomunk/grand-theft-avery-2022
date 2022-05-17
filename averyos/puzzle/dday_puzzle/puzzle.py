from shell.env import ENV
from .ciphers.ciphers import build_cipher_graph
from system.usrbin_programs import usrbin_progs


def build_graph():
    # Setup ENV
    ENV.reset()
    ENV.path = usrbin_progs()

    # Build graph
    cipher_nodes, cipher_mesh = build_cipher_graph()
    root = cipher_nodes[0]

    # Combine meshes
    mesh = cipher_mesh
    ENV.plotter = mesh
    
    return root, "AveryOS (TODO - UPDATE)"
