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
        self.offset = 0

    # NOTE: assumes that this widget is always active.
    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()
        elif event.type == pg.MOUSEWHEEL:
            self.offset = max(0, self.offset - event.y)

    def update(self):
        pass

    # TODO: Turn hard-coded adjustments into constants
    def draw(self, surf: pg.Surface):
        iw = self.image.get_width()
        sw = surf.get_width() + 20
        if iw > sw:
            h = int(self.image.get_height() * sw / iw)
            self.image = pg.transform.scale(self.image, (sw, h))
        
        ih = self.image.get_height()
        sh = surf.get_height()
        self.offset = max(0, min(self.offset, ih - sh))
        x, y = self.pos
        y -= self.offset

        surf.blit(self.image, (x,y))

        # Draw hint
        hint = FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT)
        surf.blit(hint, (surf.get_width() - hint.get_width() - 10, 10))
