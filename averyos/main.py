import sys
import pygame as pg

from shell.shell import Shell
from puzzle.test_puzzle1 import test_puzzle1

from gui.view import SplitView
from gui.window import OSWindow


if __name__ == '__main__':
    root = test_puzzle1()
    shell = Shell(root)

    pg.init()

    clock = pg.time.Clock()
    gui = OSWindow(shell)

    def show_nav(event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RALT:
                if gui.viewtag != "nav":
                    new_view = SplitView(None, gui.terminal, gui.size, weight=0.2, bg_color1=(50,50,50))
                    gui.push_view("nav", new_view)
            if event.key == pg.K_RCTRL:
                gui.pop_view()

    gui.add_event_listener(show_nav)

    running = True
    while running:
        running = gui.update()
        gui.draw()

        pg.display.flip()
        clock.tick(30)
