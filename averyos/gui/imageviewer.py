import pygame as pg

from gui.widget import Widget
from gui.constants import Colors, Fonts


COLOR_OUT = Colors.TXT_OUT
FONT_HINT = Fonts.HINT


class ImageViewerWidget(Widget):

    def __init__(self, filepath, on_finish, pos=(20,20)):
        self.pos = pos
        self.finish_cb = on_finish
        self.image = pg.image.load(filepath).convert_alpha()
        self.offset = 0

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
        sw = surf.get_width() - 2*self.pos[0]
        if iw > sw:
            h = int(self.image.get_height() * sw / iw)
            self.image = pg.transform.scale(self.image, (sw, h))
        
        # Compute offset
        ih = self.image.get_height()
        sh = surf.get_height()
        self.offset = max(0, min(self.offset, ih - sh + 2*self.pos[1]))

        # Draw at offset shifted position and view
        x = self.pos[0] + (sw - iw) // 2
        if ih < sh - 2*self.pos[1]:
            y = (sh - ih) // 2
        else:
            y = max(0, self.pos[1] - self.offset)
        ofs = self.offset - self.pos[1] if y <= 0 else 0
        surf.blit(self.image, (x,y), pg.Rect(0,ofs,sw,sh))

        # Draw hint
        hint = FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT)
        surf.blit(hint, (surf.get_width() - hint.get_width() - 10, 10))
