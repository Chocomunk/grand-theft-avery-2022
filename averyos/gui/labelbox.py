import pygame as pg

from shell.env import ENV
from gui.widget import Widget


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
FONT = pg.font.SysFont('Consolas', 16)      # Must be a uniform-sized "terminal font"


# TODO: Support scrolling
class LabelBoxWidget(Widget):

    def __init__(self, text, on_finish, pos=(20,20), line_spacing=5, par_spacing=10):
        self.pos = pos
        self.finish_cb = on_finish
        self.line_spacing = line_spacing
        self.par_spacing = par_spacing

        self.text = text
        self.lines = text.split('\n')

    # NOTE: assumes that this widget is always active.
    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()

    # TODO: maybe update the text range when scrolling is implemented
    def update(self):
        pass

    def draw(self, surf: pg.Surface):
        surfs = []
        width, height = 0, 0
        for line in self.lines:
            if not line:
                height += self.par_spacing
                surfs.append(None)
            else:
                txt_surf = FONT.render(line, True, COLOR_OUT)
                height += txt_surf.get_height() + self.line_spacing
                width = max(width, txt_surf.get_width())
                surfs.append(txt_surf)

        tmp_surf = pg.Surface((width, height), pg.SRCALPHA, 32)
        
        x = 0
        y = 0
        for txt_surf in surfs:
            if not txt_surf:
                y += self.par_spacing
            else:
                tmp_surf.blit(txt_surf, (x, y))
                y += txt_surf.get_height() + self.line_spacing

        surf.blit(tmp_surf, self.pos)
