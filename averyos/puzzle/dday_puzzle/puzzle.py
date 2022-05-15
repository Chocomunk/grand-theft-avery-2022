from shell.env import ENV
from puzzle.dday_puzzle.ciphers.ciphers import build_cipher_graph


def build_graph():
    root, mesh = build_cipher_graph()
    ENV.plotter = mesh
    return root, "AveryOS (TODO - UPDATE)"
