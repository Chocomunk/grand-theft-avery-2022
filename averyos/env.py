from typing import Dict, List

from filesystem import Node
from program import ProgramBase


class ENV:

    prompt_base = "[{pwd}]> "
    path: Dict[str, ProgramBase] = {}

    log = None

    curr_node: Node = None
    node_history: List[Node] = []       # Does not include curr_node

    @classmethod
    def reset(cls):
        cls.prompt_base = "[{pwd}]> "
        cls.path = {}
        cls.log = None
        cls.curr_node = None
        cls.node_history = []