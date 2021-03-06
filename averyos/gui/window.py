import sys
import traceback
from typing import Any, Callable, List

import pygame as pg

from shell.shell import Shell
from shell.copy_logger import CopyLogger, LogType, LinesLog

from gui.view import MainView
from gui.terminal import TerminalWidget
from gui.widget import Widget
from gui.constants import Colors


class Window:

    def __init__(self, size, flags=0, bg_color=(255, 255, 255)) -> None:
        self.screen = pg.display.set_mode(size, flags)
        self.view = MainView(self.screen.get_size())
        self.bg_color = bg_color
        self.size = self.screen.get_size()

        self.event_cbs: List[Callable[[pg.event.Event], Any]] = []

    def add_event_listener(self, func: Callable[[pg.event.Event], Any]):
        self.event_cbs.append(func)

    def update(self):
        for event in pg.event.get():
            # Window event handlers
            if event.type == pg.QUIT:
                pg.quit()
                return False

            # Event callbacks
            for cb in self.event_cbs:
                cb(event)

            # View's event handler
            self.view.handle_event(event)

        # View update
        self.view.update()

        return True

    def draw(self):
        self.screen.fill(self.bg_color)
        self.view.draw(self.screen)


class OSWindow(Window):

    MAIN_TAG = "__MAIN__"

    def __init__(self, shell: Shell, bg_color=Colors.BACKGROUND) -> None:
        # OS window is always fullscreen
        super().__init__((0, 0), pg.FULLSCREEN, bg_color)

        # Initialize state
        w, h = self.size
        self.shell = shell
        self.shell.set_gui(self)

        # Initialize terminal widget
        self.terminal = TerminalWidget(0, 0, w, h, 
                            prompt_func=shell.prompt, file=LinesLog())
        self.terminal.active = True
        sys.stdout = self.terminal.file
        sys.stderr = CopyLogger(file=sys.stderr, 
                                logdata=self.terminal.file, logtype=LogType.ERR)
        self.terminal.add_input_listener(shell.handle_input)

        # Add terminal to the default MainView
        self.view.add_widget(self.terminal)

        # Initialize view stack
        self.viewstack = []
        self.viewtag = OSWindow.MAIN_TAG

        # Start shell
        shell.start()

    # TODO: Consider ways to handle repeat tags
    def push_view(self, tag, view: Widget):
        """ 
        Push and render the view. The `tag` parameter is used to identify views,
        it can be any type that supports equality comparisons.
        """
        self.viewstack.append((self.viewtag, self.view))
        self.view = view
        self.viewtag = tag

    def pop_view(self):
        if len(self.viewstack) > 0:
            self.viewtag, self.view = self.viewstack.pop()
        else:

            # NOTE: Print exception to console without really raising
            try:
                raise IndexError("View stack is empty!")
            except:
                traceback.print_exc(file=sys.__stderr__)