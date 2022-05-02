import sys
from typing import List

import pygame as pg

from shell.shell import Shell
from gui.terminal import TerminalSurface
from gui.widget import Widget, WidgetStatus
from shell.copy_logger import CopyLogger, LogType, LinesLog


class Window:

    def __init__(self, size, flags=0, bg_color=((255, 255, 255))) -> None:
        self.win = pg.display.set_mode(size, flags)
        self.widgets: List[Widget] = []
        self.bg_color = bg_color

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
            for el in self.widgets:
                if el.handle_event(event) == WidgetStatus.EXIT:
                    return False

        for el in self.widgets:
            if el.update() == WidgetStatus.EXIT:
                return False

        return True

    def render(self):
        self.win.fill(self.bg_color)
        for el in self.widgets:
            el.draw(self.win)


# TODO: Use views
class OSWindow(Window):

    def __init__(self, shell: Shell, bg_color=(30, 30, 30)) -> None:
        # OS window is always fullscreen
        super().__init__((0, 0), pg.FULLSCREEN, bg_color)

        self.shell = shell

        self.terminal = TerminalSurface(0, 0, 
                            self.win.get_width(), self.win.get_height(), 
                            prompt_func=shell.prompt, file=LinesLog())
        self.terminal.active = True
        sys.stdout = self.terminal.file
        sys.stderr = CopyLogger(file=sys.stderr, 
                                logdata=self.terminal.file, logtype=LogType.ERR)
        self.terminal.add_input_listener(shell.handle_input)

        self.widgets.append(self.terminal)
