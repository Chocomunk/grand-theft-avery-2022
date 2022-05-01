import sys
import pygame as pg

from shell.shell import Shell
from shell.copy_logger import LinesLog, CopyLogger, LogType
from puzzle.test_puzzle1 import test_puzzle1

from gui.os_window import OSWindow
from gui.terminal import TerminalSurface


if __name__ == '__main__':
    root = test_puzzle1()
    shell = Shell(root)

    pg.init()

    clock = pg.time.Clock()
    gui = OSWindow((640, 480))

    terminal = TerminalSurface(0, 0, 640, 480, 
                                prompt_func=shell.prompt, file=LinesLog())
    terminal.active = True
    sys.stdout = terminal.file
    sys.stderr = CopyLogger(file=sys.stderr, 
                            logdata=terminal.file, logtype=LogType.ERR)

    gui.elements.append(terminal)

    terminal.add_input_listener(shell.handle_input)

    running = True
    while running:
        running = gui.update()
        gui.render()

        pg.display.flip()
        clock.tick(30)
