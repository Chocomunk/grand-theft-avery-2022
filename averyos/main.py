import pygame as pg

from shell.shell import Shell
from puzzle.test_puzzle.test_puzzle1 import test_puzzle1

from gui.window import OSWindow


if __name__ == '__main__':
    root, msg = test_puzzle1()
    shell = Shell(root, msg)

    pg.init()

    clock = pg.time.Clock()
    gui = OSWindow(shell)

    # NOTE: Can also show nav by calling "ls"
    def show_nav(event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RALT:
                shell.handle_input("ls")

    gui.add_event_listener(show_nav)

    running = True
    while running:
        running = gui.update()
        if running:
            gui.draw()

            pg.display.flip()
            clock.tick(30)
