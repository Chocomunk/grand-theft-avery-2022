from typing import List

from shell.env import ENV
from gui.plotter import MeshPlotter

from system.program import ExitCode
from system.usrbin_programs import CLIProgramBase
from system.filesystem import Node

from .fanfic_files import *


class SkipTo(CLIProgramBase):

    NAME = "FORCE_SKIP_TO_END"

    def __init__(self, to_node: Node, hidden=False):
        super().__init__(hidden)
        self.to_node: Node = to_node

    def cli_main(self, args) -> ExitCode:
        # Ignore locks and just chdir to new_node
        ENV.node_history.append(ENV.curr_node)
        ENV.visited_nodes.add(self.to_node)
        ENV.curr_node = self.to_node
        self.to_node.call_entry_callbacks()
        return ExitCode.OK


class FanficState:

    disclaimer_opened = False
    contract_opened = False
    # Unique integer index for each node and whether it has been visited
    visited = {i: False for i in range(24)}


def build_fanfic_graph():
    # Entry
    root = Node("forbidden-mathematical-relations")
    root.directory.add_file(disclaimer)
    def _disclaimer_open():
        FanficState.disclaimer_opened = True
    disclaimer.add_open_callback(_disclaimer_open)

    # Visit node
    def visit(i):
        def _func(_):
            FanficState.visited[i] = True
        return _func

    def view_text(text):
        return lambda _: print(text)

    # Keep track of visited node index (as ordered in this file)
    nodes: List[Node] = []
    i = 0

    # begin
    begin = Node("begin-journey", parents=[root])
    begin.set_lock_func(lambda _: not FanficState.disclaimer_opened)
    begin.directory.add_file(dinakars_lair)
    begin.directory.add_file(whoareyou)
    begin.directory.add_file(contract)
    begin.add_entry_callback(visit(i))
    nodes.append(begin)
    i += 1
    
    def _contract_open():
        FanficState.contract_opened = True
    contract.add_open_callback(_contract_open)

    # chalk
    chalk = Node("bitch-about-chalk", parents=[begin])
    chalk.set_lock_func(lambda _: not FanficState.contract_opened)
    chalk.directory.add_file(dinakars_strife)
    chalk.directory.add_file(smug_voice)
    chalk.add_entry_callback(view_text(chalk_text))
    chalk.add_entry_callback(visit(i))
    nodes.append(chalk)
    i += 1

    # continue_work
    continue_work = Node("continue-working", parents=[chalk])
    continue_work.directory.add_file(irresistible_temptation)
    continue_work.add_entry_callback(visit(i))
    nodes.append(continue_work)
    i += 1

    # respond
    respond = Node("respond", parents=[chalk, continue_work])
    respond.directory.add_file(questioning_figure)
    respond.directory.add_file(legend_revealed)
    respond.add_entry_callback(visit(i))
    nodes.append(respond)
    i += 1

    # drop_knees
    drop_knees = Node("drop-to-your-knees", parents=[respond])
    drop_knees.directory.add_file(showing_reverence)
    drop_knees.add_entry_callback(view_text(drop_knees_text))
    drop_knees.add_entry_callback(visit(i))
    nodes.append(drop_knees)
    i += 1

    # shock
    shock = Node("stand-in-shock", parents=[respond, drop_knees])
    shock.directory.add_file(katzs_admonishment)
    shock.add_entry_callback(visit(i))
    nodes.append(shock)
    i += 1

    # continue_standing
    continue_standing = Node("continue-standing-still", parents=[shock])
    continue_standing.directory.add_file(legend_approaches)
    continue_standing.directory.add_file(legend_inquires)
    continue_standing.directory.add_file(dinakars_feelings)
    continue_standing.add_entry_callback(visit(i))
    nodes.append(continue_standing)
    i += 1

    # expose
    expose_i = i
    expose = Node("expose-yourself", parents=[shock, continue_standing])
    expose.directory.add_file(dinakars_package)
    expose.directory.add_file(did_it_again)
    def _expose_file_toggle(_: Node):
        if FanficState.visited[expose_i]:
            dinakars_package.hidden = True
            did_it_again.hidden = False
        else:
            print(surprised_pikachu)
    expose.add_entry_callback(_expose_file_toggle)
    expose.add_entry_callback(visit(i))
    nodes.append(expose)
    i += 1

    # step_back
    step_back = Node("step-back", parents=[continue_standing])
    step_back.directory.add_file(attempted_retreat)
    step_back.add_entry_callback(visit(i))
    nodes.append(step_back)
    i += 1

    # converse
    converse = Node("converse", parents=[step_back])
    converse.directory.add_file(revelation)
    converse.add_entry_callback(visit(i))
    nodes.append(converse)
    i += 1

    # flirt
    flirt = Node("flirt", parents=[continue_standing, expose])
    flirt.directory.add_file(dinakars_gamble)
    flirt.add_entry_callback(view_text(flirt_text))
    flirt.add_entry_callback(visit(i))
    nodes.append(flirt)
    i += 1

    # get_boi
    get_boi = Node("lets-get-this-boi", parents=[flirt])
    get_boi.directory.add_file(pickup_line)
    get_boi.add_entry_callback(visit(i))
    nodes.append(get_boi)
    i += 1

    # reel_in
    reel_in = Node("time-to-reel-him-in", parents=[get_boi])
    reel_in.directory.add_file(hell)
    reel_in.add_entry_callback(visit(i))
    nodes.append(reel_in)
    i += 1

    # kiss
    kiss = Node("kiss", parents=[step_back])
    kiss.directory.add_file(dinakars_move)
    kiss.add_entry_callback(visit(i))
    nodes.append(kiss)
    i += 1

    # lets_begin
    lets_begin = Node("lets-begin", parents=[reel_in, converse])
    lets_begin.directory.add_file(it_begins)
    lets_begin.add_entry_callback(view_text(lets_begin_text))
    lets_begin.add_entry_callback(visit(i))
    nodes.append(lets_begin)
    i += 1

    # passion 
    passion = Node("enter-the-throes-of-passion", parents=[lets_begin])
    passion.directory.add_file(proposition)
    passion.directory.add_file(beginning_of_love)
    passion.add_entry_callback(visit(i))
    nodes.append(passion)
    i += 1

    # intensify
    intensify = Node("intensify", parents=[kiss, passion])
    intensify.directory.add_file(french_kiss)
    intensify.add_entry_callback(visit(i))
    nodes.append(intensify)
    i += 1

    # dragon
    dragon = Node("release-the-dragon", parents=[intensify])
    dragon.directory.add_file(exposure)
    dragon.add_entry_callback(view_text(shitpost_face))
    dragon.add_entry_callback(visit(i))
    nodes.append(dragon)
    i += 1

    # silent
    silent = Node("remain-silent", parents=[dragon])
    silent.directory.add_file(examination)
    silent.add_entry_callback(visit(i))
    nodes.append(silent)
    i += 1

    # boast
    boast = Node("boast-about-your-size", parents=[dragon])
    boast.directory.add_file(dinakars_tease)
    boast.add_entry_callback(visit(i))
    nodes.append(boast)
    i += 1

    # control
    control = Node("let-nets-take-control", parents=[boast])
    control.directory.add_file(nets_tease)
    control.add_entry_callback(visit(i))
    nodes.append(control)
    i += 1

    # want
    want = Node("tell-him-that-you-want-it", parents=[control, silent])
    want.directory.add_file(dinakars_desire)
    want.add_entry_callback(visit(i))
    nodes.append(want)
    i += 1

    # enter
    enter = Node("enter-nets", parents=[want])
    enter.directory.add_file(wide_mouth)
    enter.add_entry_callback(visit(i))
    nodes.append(enter)
    i += 1

    # climax 
    climax = Node("climax", parents=[enter])
    climax.directory.add_file(eruption)
    climax.add_entry_callback(visit(i))
    nodes.append(climax)
    i += 1

    # finish
    finish = Node("finish-up", parents=[climax])
    finish.directory.add_file(resolution)
    nodes.append(finish)

    # return_favor
    return_favour = Node("return-the-favor", parents=[climax])
    return_favour.set_lock_func(lambda _: not all(FanficState.visited.values()))
    return_favour.directory.add_file(continuation)
    return_favour.directory.add_file(want_to_read_more)
    return_favour.directory.add_file(too_far_to_stop)
    return_favour.add_entry_callback(view_text(return_favor_text))
    nodes.append(return_favour)

    # last_thought
    last_thought = Node("last-thought", parents=[return_favour])
    last_thought.add_entry_callback(view_text(last_thought_text))
    nodes.append(last_thought)

    # end 
    end = Node("end-story", parents=[finish, last_thought])

    skip_prog = SkipTo(end)
    for n in nodes:
        n.directory.add_program(skip_prog.NAME, skip_prog)

    return [root] + nodes, None
