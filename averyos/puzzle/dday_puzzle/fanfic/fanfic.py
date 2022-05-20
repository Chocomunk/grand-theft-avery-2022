import sys

from shell.env import ENV
from puzzle.util import add_dir_files

from gui.plotter import MeshPlotter
from system.filesystem import File, Node
from system.usrbin_programs import Chdir, Chdirid, ReadFile, Render, ListNode

from puzzle.dday_puzzle.programs.prompt_password import UnlockPromptPassword

from .fanfic_files import *


class FanficState:

    disclaimer_opened = False


def build_fanfic_graph():
    # Entry
    # root = Node("forbidden-mathematical-relations")
    root = Node("fmr")
    root.directory.add_file(disclaimer)
    def _disclaimer_open():
        FanficState.disclaimer_opened = True
    disclaimer.add_open_callback(_disclaimer_open)

    # begin
    begin = Node("begin-journey", parents=[root])
    begin.set_lock_func(lambda _: not FanficState.disclaimer_opened)



    return [root], None