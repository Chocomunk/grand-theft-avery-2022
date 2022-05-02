import sys
import pygame as pg

from shell.shell import Shell
from shell.copy_logger import LinesLog, CopyLogger, LogType
from puzzle.test_puzzle1 import test_puzzle1

from gui.window import OSWindow


if __name__ == '__main__':
    root = test_puzzle1()
    shell = Shell(root)

    pg.init()

    clock = pg.time.Clock()
    gui = OSWindow(shell)

    running = True
    while running:
        running = gui.update()
        gui.draw()

        pg.display.flip()
        clock.tick(30)
