import sys
import pygame as pg
from pygame import Surface
from typing import Callable, List

from gui.widget import Widget
from shell.copy_logger import LinesLog, LogType


# TODO: Clean up color and font handling
pg.init()
COLOR_CURSOR = pg.Color(230,230,230,100)
COLOR_OUT = pg.Color('lightskyblue3')
COLOR_ERR = pg.Color('firebrick1')
COLOR_IN = pg.Color('darkolivegreen1')
FONT = pg.font.SysFont('Consolas', 16)      # Must be a uniform-sized "terminal font"
TXT_W, TXT_H = FONT.size("O")


# TODO: allow scrolling past the end. Snap to the end when typing
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

        self.offset = 0
        self.cmd_hist = []
        self.hist_idx = 0

        self.cursor = len(self.text)

        self.active = False

        # Allow for holding down a key
        pg.key.set_repeat(400, 30)

    def add_input_listener(self, func):
        self.input_cbs.append(func)

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pg.MOUSEWHEEL:
            self.offset = max(0, self.offset + event.y)

        if event.type == pg.KEYDOWN:
            if self.active:

                # Scroll command history
                if event.key == pg.K_UP:
                    if len(self.cmd_hist) > 0:  # (this 'if' must be inside for cursor to work)
                        self.hist_idx = max(0, self.hist_idx-1)
                        self.text = self.cmd_hist[self.hist_idx]
                elif event.key == pg.K_DOWN:
                    if len(self.cmd_hist) > 0:
                        if self.hist_idx < len(self.cmd_hist) - 1:
                            self.hist_idx = min(len(self.cmd_hist) - 1, self.hist_idx+1)
                            self.text = self.cmd_hist[self.hist_idx]
                        else:
                            self.text = ""      # Went past the newest history

                # Move cursor
                elif event.key == pg.K_LEFT:
                    self.cursor = max(0, self.cursor - 1)
                elif event.key == pg.K_RIGHT:
                    self.cursor = min(len(self.text), self.cursor + 1)

                # Send input
                elif event.key == pg.K_RETURN:
                    self.file.write(self.prompt_func() + self.text + '\n', LogType.IN)
                    if self.text.strip():
                        self.cmd_hist.append(self.text)
                        self.hist_idx = len(self.cmd_hist)

                    # If input handler returns False, then quit
                    for cb in self.input_cbs:
                        if cb(self.text) == False:
                            quit_event = pg.event.Event(pg.QUIT)
                            pg.event.post(quit_event)

                    self.text = ''
                    self.cursor = 0

                # Type or delete text
                elif event.key == pg.K_BACKSPACE:
                    if self.cursor > 0:
                        self.text = self.text[:self.cursor-1] + self.text[self.cursor:]
                        self.cursor = max(0, self.cursor - 1)
                else:
                    c = event.unicode
                    self.text = self.text[:self.cursor] + c + self.text[self.cursor:]
                    self.cursor += len(c)

                # Return to look at current line
                self.offset = 0

    def update(self):
        # Resize the box if the text is too long.
        self.render_text()
        width = max(self.rect.w, self.txt_surf.get_width()+10)
        self.rect.w = width

    def draw(self, surf: Surface):
        surf.blit(self.txt_surf, (self.rect.x+5, self.rect.y+5))
        
    # TODO: set text color based on logtype. BAD IMPLEMENTATION
    def render_text(self):
        line_h = TXT_H + self.line_spacing
        line_len = len(self.file) + 1
        surf_lines = (self.txt_surf.get_height() // line_h)
        num_lines = min(surf_lines, line_len)

        # Disable offset if text is smaller than the surface.
        if num_lines < surf_lines:
            self.offset = 0
        else:
            self.offset = min(self.offset, line_len - num_lines)

        # Compute window of lines
        end_idx = line_len - self.offset
        start_idx = end_idx - num_lines

        # Add all lines as a surf
        self.txt_surf.fill((0, 0, 0, 0))
        draw_height = 0
        for line, t in self.file.getlines(start_idx, end_idx):
            if t == LogType.ERR:
                surf = FONT.render(line, True, COLOR_ERR)
            elif t == LogType.IN:
                surf = FONT.render(line, True, COLOR_IN)
            else:
                surf = FONT.render(line, True, COLOR_OUT)
            self.txt_surf.blit(surf, (0, draw_height))
            draw_height += surf.get_height() + self.line_spacing

        # Add current line as a surf
        if self.offset == 0:
            prompt = self.prompt_func()

            # Draw cursor
            cursor_pos = TXT_W * (len(prompt) + self.cursor)
            cursor_box = pg.Rect(cursor_pos, draw_height, TXT_W, TXT_H)
            pg.draw.rect(self.txt_surf, COLOR_CURSOR, cursor_box)

            # Draw text
            cur_line = prompt + self.text
            surf = FONT.render(cur_line, True, COLOR_IN)
            self.txt_surf.blit(surf, (0, draw_height))

