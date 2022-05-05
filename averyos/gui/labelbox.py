import sys
import pygame as pg

from gui.widget import Widget


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
FONT = pg.font.SysFont('Consolas', 16)      # Must be a uniform-sized "terminal font"
TXT_W, TXT_H = FONT.size("O")


class LabelBoxWidget(Widget):

    def __init__(self, text, on_finish, pos=(20,20), line_spacing=5):
        self.pos = pos
        self.finish_cb = on_finish
        self.line_spacing = line_spacing

        self.offset = 0
        self.text = text
        self.lines = ['a' * (i//2) for i in range(100)] + text.split('\n')

    # NOTE: assumes that this widget is always active.
    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()
        elif event.type == pg.MOUSEWHEEL:
            self.offset -= event.y

    # TODO: maybe update the text range when scrolling is implemented
    def update(self):
        pass

    # TODO: add padding
    def draw(self, surf: pg.Surface):
        line_len = len(self.lines)
        num_lines = (surf.get_height() // (TXT_H + self.line_spacing)) - 1

        # Compute window of lines
        end_idx = line_len + self.offset                    # Exclusive
        end_idx = max(num_lines, min(line_len, end_idx))    # Clamp idx
        self.offset = end_idx - line_len                    # Correct offset
        start_idx = end_idx - num_lines                     # Inclusive

        # Draw lines
        x, y = self.pos
        for line in self.lines[start_idx:end_idx]:
            if line:
                txt_surf = FONT.render(line, True, COLOR_OUT)
                surf.blit(txt_surf, (x, y))
            y += TXT_H + self.line_spacing
