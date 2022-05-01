import pygame as pg

from gui.gui_term import *
from shell.shell import Shell
from puzzle.test_puzzle1 import test_puzzle1


if __name__ == '__main__':
    root = test_puzzle1()
    shell = Shell(root)

    pg.init()

    clock = pg.time.Clock()
    gui = AveryOSWin()

    terminal = TerminalGUI(0, 0, 640, 480, prompt_func=shell.prompt)
    terminal.active = True
    sys.stdout = terminal.file
    sys.stderr = terminal.file

    gui.elements.append(terminal)

    terminal.add_input_listener(shell.handle_input)

    running = True
    while running:
        # running = shell.handle_input(input(shell.prompt()))
        running = gui.update()
        gui.render()

        pg.display.flip()
        clock.tick(30)
