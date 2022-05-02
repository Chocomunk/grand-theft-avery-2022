from typing import Dict, List

from system.filesystem import Node
from system.program import ProgramBase


class ENV:

    prompt_base = "[{pwd}]> "
    path: Dict[str, ProgramBase] = {}

    log = None
    gui = None

    curr_node: Node = None
    node_history: List[Node] = []       # Does not include curr_node

    # NOTE: Creating a shell will reset the path, which might overwrite
    #       puzzle programs that we place into the path. If this is a problem,
    #       then fix it (lol).
    @classmethod
    def reset(cls):
        cls.prompt_base = "[{pwd}]> "
        cls.path = {}
        cls.log = None
        cls.gui = None
        cls.curr_node = None
        cls.node_history = []