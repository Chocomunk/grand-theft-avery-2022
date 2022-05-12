import sys
import pygame as pg

from gui.widget import Widget


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
FONT_HINT = pg.font.SysFont('Consolas', 14)      # Must be a uniform-sized "terminal font"


# TODO: support scrolling
class ImageViewerWidget(Widget):

    def __init__(self, filepath, on_finish, pos=(20,20)):
        self.pos = pos
        self.finish_cb = on_finish
        self.image = pg.image.load(filepath).convert_alpha()

    # NOTE: assumes that this widget is always active.
    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()

    def update(self):
        pass

    # TODO: Turn hard-coded adjustments into constants
    def draw(self, surf: pg.Surface):
        surf.blit(self.image, self.pos)

        # Draw hint
        hint = FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT)
        surf.blit(hint, (surf.get_width() - hint.get_width() - 10, 10))
