import sys

import pygame as pg

from shell.shell import Shell
from shell.copy_logger import CopyLogger, LogType, LinesLog

from gui.view import MainView
from gui.terminal import TerminalWidget
from gui.widget import Widget, WidgetStatus


class Window:

    def __init__(self, size, flags=0, bg_color=((255, 255, 255))) -> None:
        self.screen = pg.display.set_mode(size, flags)
        self.view = MainView(self.screen.get_size())
        self.bg_color = bg_color
        self.size = self.screen.get_size()

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
            if self.view.handle_event(event) == WidgetStatus.EXIT:
                return False

        if self.view.update() == WidgetStatus.EXIT:
            return False

        return True

    def draw(self):
        self.screen.fill(self.bg_color)
        self.view.draw(self.screen)


class OSWindow(Window):

    def __init__(self, shell: Shell, bg_color=(30, 30, 30)) -> None:
        # OS window is always fullscreen
        super().__init__((0, 0), pg.FULLSCREEN, bg_color)

        w, h = self.size
        self.shell = shell

        self.terminal = TerminalWidget(0, 0, w, h, 
                            prompt_func=shell.prompt, file=LinesLog())
        self.terminal.active = True
        sys.stdout = self.terminal.file
        sys.stderr = CopyLogger(file=sys.stderr, 
                                logdata=self.terminal.file, logtype=LogType.ERR)
        self.terminal.add_input_listener(shell.handle_input)

        self.view.add_widget(self.terminal)
