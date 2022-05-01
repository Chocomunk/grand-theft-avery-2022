import pygame as pg
from pygame import Surface
from typing import Callable

from shell.copy_logger import LinesLog, LogType


pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.SysFont('Consolas', 14)      # Must be a uniform-sized "terminal font"


# TODO: Compute font-height and show only the latest n logs
# TODO: Allow scrolling to show the logs at [k-n, k] (n logs ending at log k)
class TerminalSurface:

    def __init__(self, x, y, w, h, 
                    text='', prompt_func=lambda: "", file=LinesLog()):
        self.file = file
        self.prompt_func = prompt_func
        self.text = text
        self.active = False
        self.input_cbs: Callable[[str], bool] = []

        self.file.write(self.prompt_func())

        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.txt_surface = FONT.render("", True, self.color)

    def add_input_listener(self, func):
        self.input_cbs.append(func)

    # TODO: set 5px padding as constant
    def render_text(self):
        # Add all lines as a surf
        total_height = 0
        max_width = 0
        surfs = []
        for line, _ in self.file.getlines():
            surf = FONT.render(line, True, self.color)
            total_height += surf.get_height() + 5
            max_width = max(max_width, surf.get_width())
            surfs.append(surf)

        # Add current line as a surf
        cur_line = self.file.get_curr_line() + self.text
        surf = FONT.render(cur_line, True, self.color)
        total_height += surf.get_height() + 5
        max_width = max(max_width, surf.get_width())
        surfs.append(surf)

        # Initialize parent surface
        # TODO: probably don't need to reinitialize
        self.txt_surface = Surface((max_width, total_height), pg.SRCALPHA, 32)
        draw_height = 0
        for surf in surfs:
            self.txt_surface.blit(surf, (0, draw_height))
            draw_height += surf.get_height() + 5

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            self.active = self.rect.collidepoint(event.pos)

            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

        if event.type == pg.KEYDOWN:
            if self.active:

                # Send input
                if event.key == pg.K_RETURN:
                    self.file.write(self.text + '\n', LogType.IN)
                    for cb in self.input_cbs:
                        if not cb(self.text):
                            return False
                    self.file.write(self.prompt_func())
                    self.text = ''

                # Type or delete text
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        return True

    def update(self):
        # Resize the box if the text is too long.
        self.render_text()
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, parent_surf: Surface):
        parent_surf.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
