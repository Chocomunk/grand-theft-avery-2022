import sys

from shell.env import ENV
from puzzle.util import add_dir_files

from gui.plotter import MeshPlotter
from system.filesystem import File, Node
from system.usrbin_programs import Chdir, Chdirid, ReadFile, Render, ListNode

from puzzle.dday_puzzle.programs.prompt_password import UnlockPromptPassword

from .fanfic_files import *


# These variables contain the ASCII art and text that appear when landing on
# certain nodes.

surprised_pikachu = \
""" 
⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⣠⣤⣶⣶
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⢰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣀⣀⣾⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡏⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠁⠀⣿
⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠙⠿⠿⠿⠻⠿⠿⠟⠿⠛⠉⠀⠀⠀⠀⠀⣸⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣴⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢰⣹⡆⠀⠀⠀⠀⠀⠀⣭⣷⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠈⠉⠀⠀⠤⠄⠀⠀⠀⠉⠁⠀⠀⠀⠀⢿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢾⣿⣷⠀⠀⠀⠀⡠⠤⢄⠀⠀⠀⠠⣿⣿⣷⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡀⠉⠀⠀⠀⠀⠀⢄⠀⢀⠀⠀⠀⠀⠉⠉⠁⠀⠀⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿
"""

shitpost_face = \
""" 
⠀⣞⢽⢪⢣⢣⢣⢫⡺⡵⣝⡮⣗⢷⢽⢽⢽⣮⡷⡽⣜⣜⢮⢺⣜⢷⢽⢝⡽⣝
⠸⡸⠜⠕⠕⠁⢁⢇⢏⢽⢺⣪⡳⡝⣎⣏⢯⢞⡿⣟⣷⣳⢯⡷⣽⢽⢯⣳⣫⠇
⠀⠀⢀⢀⢄⢬⢪⡪⡎⣆⡈⠚⠜⠕⠇⠗⠝⢕⢯⢫⣞⣯⣿⣻⡽⣏⢗⣗⠏⠀
⠀⠪⡪⡪⣪⢪⢺⢸⢢⢓⢆⢤⢀⠀⠀⠀⠀⠈⢊⢞⡾⣿⡯⣏⢮⠷⠁⠀⠀
⠀⠀⠀⠈⠊⠆⡃⠕⢕⢇⢇⢇⢇⢇⢏⢎⢎⢆⢄⠀⢑⣽⣿⢝⠲⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡿⠂⠠⠀⡇⢇⠕⢈⣀⠀⠁⠡⠣⡣⡫⣂⣿⠯⢪⠰⠂⠀⠀⠀⠀
⠀⠀⠀⠀⡦⡙⡂⢀⢤⢣⠣⡈⣾⡃⠠⠄⠀⡄⢱⣌⣶⢏⢊⠂⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢝⡲⣜⡮⡏⢎⢌⢂⠙⠢⠐⢀⢘⢵⣽⣿⡿⠁⠁⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠨⣺⡺⡕⡕⡱⡑⡆⡕⡅⡕⡜⡼⢽⡻⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣼⣳⣫⣾⣵⣗⡵⡱⡡⢣⢑⢕⢜⢕⡝⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣴⣿⣾⣿⣿⣿⡿⡽⡑⢌⠪⡢⡣⣣⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⡟⡾⣿⢿⢿⢵⣽⣾⣼⣘⢸⢸⣞⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠁⠇⠡⠩⡫⢿⣝⡻⡮⣒⢽⠋⠀
"""

chalk_text = \
""" 
Looks like you sickos actually want to go through with this…
"""

drop_knees_text = \
""" 
I guess Katz’s heavenly presence really touched you, huh?
"""

expose_text = \
""" 
The fuck’s your obsession with Dinakar exposing himself, you creep?
"""

flirt_text = \
""" 
You sly dog ;)
"""

lets_begin_text = \
""" 
You might want to loosen your belt and untuck your shirt for what’s to come. It’s going to get hot in here…
"""

return_favor_text = \
""" 
Congratulations you pervert! You explored all possible paths in this godforsaken story, so here’s a little epilogue to satisfy you.
"""

last_thought_text = \
""" 
“Thank god men can’t get pregnant.”
"""


class FanficState:

    disclaimer_opened = False
    # Unique integer index for each node and whether it has been visited
    visited = {i: False for i in range(24)}


def build_fanfic_graph():
    # Entry
    # root = Node("forbidden-mathematical-relations")
    root = Node("fmr")
    root.directory.add_file(disclaimer)
    def _disclaimer_open():
        FanficState.disclaimer_opened = True
    disclaimer.add_open_callback(_disclaimer_open)

    # Keep track of visited node index (as ordered in this file)
    i = 0

    # Visit node
    def visit(i):
        FanficState.visited[i] = True

    # begin
    begin = Node("begin-journey", parents=[root])
    begin.set_lock_func(lambda _: not FanficState.disclaimer_opened)
    begin.directory.add_file(dinakars_lair)
    begin.directory.add_file(whoareyou)
    begin.directory.add_file(contract)
    begin.add_entry_callback(lambda _: visit(i))
    i += 1

    # chalk
    chalk = Node("bitch-about-chalk", parents=[begin])
    chalk.directory.add_file(dinakars_strife)
    chalk.directory.add_file(smug_voice)
    chalk.add_entry_callback(lambda _: visit(i))
    i += 1

    # continue_work
    continue_work = Node("continue-working", parents=[chalk])
    continue_work.directory.add_file(irresistible_temptation)
    continue_work.add_entry_callback(lambda _: visit(i))
    i += 1

    # respond
    respond = Node("respond", parents=[chalk, continue_work])
    respond.directory.add_file(questioning_figure)
    respond.directory.add_file(legend_revealed)
    respond.add_entry_callback(lambda _: visit(i))
    i += 1

    # drop_knees
    drop_knees = Node("drop-to-your-knees", parents=[respond])
    drop_knees.directory.add_file(showing_reverence)
    drop_knees.add_entry_callback(lambda _: visit(i))
    i += 1

    # shock
    shock = Node("stand-in-shock", parents=[respond, drop_knees])
    shock.directory.add_file(katzs_admonishment)
    shock.add_entry_callback(lambda _: visit(i))
    i += 1

    # continue_standing
    continue_standing = Node("continue-standing-still", parents=[shock])
    continue_standing.directory.add_file(legend_approaches)
    continue_standing.directory.add_file(legend_inquires)
    continue_standing.directory.add_file(dinakars_feelings)
    continue_standing.add_entry_callback(lambda _: visit(i))
    i += 1

    # expose
    expose = Node("expose-yourself", parents=[shock, continue_standing])
    # TODO: Add files based on occurrences; write callback
    expose.add_entry_callback(lambda _: visit(i))
    i += 1

    # step_back
    step_back = Node("step-back", parents=[continue_standing])
    step_back.directory.add_file(attempted_retreat)
    step_back.add_entry_callback(lambda _: visit(i))
    i += 1

    # converse
    converse = Node("converse", parents=[step_back])
    converse.directory.add_file(revelation)
    converse.add_entry_callback(lambda _: visit(i))
    i += 1

    # flirt
    flirt = Node("flirt", parents=[continue_standing, expose])
    flirt.directory.add_file(dinakars_gamble)
    flirt.add_entry_callback(lambda _: visit(i))
    i += 1

    # get_boi
    get_boi = Node("lets-get-this-boi", parents=[flirt])
    get_boi.directory.add_file(pickup_line)
    get_boi.add_entry_callback(lambda _: visit(i))
    i += 1

    # reel_in
    reel_in = Node("time-to-reel-him-in", parents=[get_boi])
    reel_in.directory.add_file(hell)
    reel_in.add_entry_callback(lambda _: visit(i))
    i += 1

    # kiss
    kiss = Node("kiss", parents=[step_back])
    kiss.directory.add_file(dinakars_move)
    kiss.add_entry_callback(lambda _: visit(i))
    i += 1

    # lets_begin
    lets_begin = Node("lets-begin", parents=[reel_in, converse])
    lets_begin.directory.add_file(it_begins)
    lets_begin.add_entry_callback(lambda _: visit(i))
    i += 1

    # passion 
    passion = Node("enter-the-throes-of-passion", parents=[lets_begin])
    passion.directory.add_file(proposition)
    passion.directory.add_file(beginning_of_love)
    passion.add_entry_callback(lambda _: visit(i))
    i += 1

    # intensify
    intensify = Node("intensify", parents=[kiss, passion])
    intensify.directory.add_file(french_kiss)
    intensify.add_entry_callback(lambda _: visit(i))
    i += 1

    # dragon
    dragon = Node("release-the-dragon", parents=[intensify])
    dragon.directory.add_file(exposure)
    dragon.add_entry_callback(lambda _: visit(i))
    i += 1

    # silent
    silent = Node("remain-silent", parents=[dragon])
    silent.directory.add_file(examination)
    silent.add_entry_callback(lambda _: visit(i))
    i += 1

    # boast
    boast = Node("boast-about-your-size", parents=[dragon])
    boast.directory.add_file(dinakars_tease)
    boast.add_entry_callback(lambda _: visit(i))
    i += 1

    # control
    control = Node("let-nets-take-control", parents=[boast])
    control.directory.add_file(nets_tease)
    control.add_entry_callback(lambda _: visit(i))
    i += 1

    # want
    want = Node("tell-him-that-you-want-it", parents=[control, silent])
    want.directory.add_file(dinakars_desire)
    want.add_entry_callback(lambda _: visit(i))
    i += 1

    # enter
    enter = Node("enter-nets", parents=[want])
    enter.directory.add_file(wide_mouth)
    enter.add_entry_callback(lambda _: visit(i))
    i += 1

    # climax 
    climax = Node("climax", parents=[enter])
    climax.directory.add_file(eruption)
    climax.add_entry_callback(lambda _: visit(i))
    i += 1

    # finish
    finish = Node("finish-up", parents=[climax])
    finish.directory.add_file(resolution)

    # return_favor
    return_favour = Node("return-the-favor", parents=[climax])
    return_favour.set_lock_func(lambda _: not all(FanficState.visited.values()))
    return_favour.directory.add_file(continuation)
    return_favour.directory.add_file(want_to_read_more)
    return_favour.directory.add_file(too_far_to_stop)

    # last_thought
    last_thought = Node("last-thought", parents=[return_favour])

    # end 
    end = Node("end-story", parents=[finish, last_thought])


    return [root], None
