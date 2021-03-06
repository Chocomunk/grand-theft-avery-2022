from typing import Dict, List, Set

from system.filesystem import Node
from system.program import ProgramBase

from gui.plotter import Plotter, GridPlotter


class ENV:

    prompt_base = "[{pwd}]> "
    path: Dict[str, ProgramBase] = {}
    visible_progs: Set[str] = set()

    log = None

    curr_node: Node = None
    node_history: List[Node] = []       # Does not include curr_node
    visited_nodes: Set[Node] = set()    # Set of all nodes that have been visited
    plotter: Plotter = GridPlotter()    # Graph plotter

    # NOTE: Creating a shell will reset the path, which might overwrite
    #       puzzle programs that we place into the path. If this is a problem,
    #       then fix it (lol).
    @classmethod
    def reset(cls):
        cls.prompt_base = "[{pwd}]> "
        cls.path = {}
        cls.visible_progs = set()
        cls.log = None
        cls.gui = None
        cls.curr_node = None
        cls.node_history = []
        cls.visited_nodes = set()
        cls.plotter = GridPlotter()