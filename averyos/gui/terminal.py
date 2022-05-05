import sys
import pygame as pg
from pygame import Surface
from typing import Callable, List

from gui.widget import Widget
from shell.copy_logger import LinesLog, LogType


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
COLOR_ERR = pg.Color('firebrick1')
COLOR_IN = pg.Color('darkolivegreen1')
FONT = pg.font.SysFont('Consolas', 16)      # Must be a uniform-sized "terminal font"


# TODO: Compute font-height and show only the latest n logs
# TODO: Allow scrolling to show the logs at [k-n, k] (n logs ending at log k)
class TerminalWidget(Widget):

    def __init__(self, x, y, w, h, 
                    text='', line_spacing=5,
                    prompt_func=lambda: "", file=LinesLog()):
        self.file = file
        self.prompt_func = prompt_func
        self.text = text
        self.line_spacing = line_spacing
        self.input_cbs: List[Callable[[str], bool]] = []

        self.rect = pg.Rect(x, y, w, h)
        self.txt_surf = Surface((w, h), pg.SRCALPHA, 32)

        self.active = False

        # Allow for holding down a key
        pg.key.set_repeat(400, 30)

    def add_input_listener(self, func):
        self.input_cbs.append(func)

    # TODO: set text color based on logtype. BAD IMPLEMENTATION
    def render_text(self):
        # Add all lines as a surf
        total_height = 0
        surfs = []
        for line, t in self.file.getlines():
            if t == LogType.ERR:
                surf = FONT.render(line, True, COLOR_ERR)
            elif t == LogType.IN:
                surf = FONT.render(line, True, COLOR_IN)
            else:
                surf = FONT.render(line, True, COLOR_OUT)
            total_height += surf.get_height() + self.line_spacing
            surfs.append(surf)

        # Add current line as a surf
        cur_line = self.prompt_func() + self.text
        surf = FONT.render(cur_line, True, COLOR_IN)
        total_height += surf.get_height() + self.line_spacing
        surfs.append(surf)

        # Initialize parent surface
        # TODO: probably don't need to reinitialize
        tmp_surf = Surface((self.rect.w, total_height), pg.SRCALPHA, 32)
        draw_height = 0
        for surf in surfs:
            tmp_surf.blit(surf, (0, draw_height))
            draw_height += surf.get_height() + self.line_spacing

        self.txt_surf.fill((0, 0, 0, 0))
        render_height = min(0, self.txt_surf.get_height() - tmp_surf.get_height() - 5)
        self.txt_surf.blit(tmp_surf, (0, render_height))

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pg.KEYDOWN:
            if self.active:

                # Send input
                if event.key == pg.K_RETURN:
                    self.file.write(self.prompt_func() + self.text + '\n', LogType.IN)

                    # If input handler returns False, then quit
                    for cb in self.input_cbs:
                        if cb(self.text) == False:
                            quit_event = pg.event.Event(pg.QUIT)
                            pg.event.post(quit_event)

                    self.text = ''

                # Type or delete text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        # Resize the box if the text is too long.
        self.render_text()
        width = max(self.rect.w, self.txt_surf.get_width()+10)
        self.rect.w = width

    def draw(self, surf: Surface):
        surf.blit(self.txt_surf, (self.rect.x+5, self.rect.y+5))
