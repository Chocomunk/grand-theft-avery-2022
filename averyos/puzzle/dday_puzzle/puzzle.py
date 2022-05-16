from shell.env import ENV
from puzzle.dday_puzzle.ciphers.ciphers import build_cipher_graph


def build_graph():
    cipher_nodes, cipher_mesh = build_cipher_graph()

    root = cipher_nodes[0]
    mesh = cipher_mesh

    ENV.plotter = mesh
    return root, "AveryOS (TODO - UPDATE)"
