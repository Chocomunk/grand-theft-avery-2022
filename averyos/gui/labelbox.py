import sys
import pygame as pg

from gui.widget import Widget


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
FONT = pg.font.SysFont('Consolas', 16)      # Must be a uniform-sized "terminal font"
FONT_HINT = pg.font.SysFont('Consolas', 14)      # Must be a uniform-sized "terminal font"
TXT_W, TXT_H = FONT.size("O")


# TODO: Fix splitview sizing
class LabelBoxWidget(Widget):

    def __init__(self, text, on_finish, pos=(20,20), line_spacing=5):
        self.pos = pos
        self.finish_cb = on_finish
        self.line_spacing = line_spacing

        self.offset = 0
        self.text = text
        self.lines = ['' if i%20==0 else 'a' * (i//2) for i in range(2, 100)] + text.split('\n')
        # self.lines = text.split('\n')

    # NOTE: assumes that this widget is always active.
    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()
        elif event.type == pg.MOUSEWHEEL:
            self.offset = max(0, self.offset - event.y)

    def update(self):
        pass

    # TODO: Draw hint at top-left
    # TODO: Turn hard-coded adjustments into constants
    def draw(self, surf: pg.Surface):
        line_h = TXT_H + self.line_spacing
        line_len = len(self.lines)
        surf_lines = (surf.get_height() // line_h)
        num_lines = min(surf_lines + 1, line_len)

        # Disable offset if text is smaller than the surface.
        if num_lines < surf_lines:
            self.offset = 0
        else:
            self.offset = min(self.offset, line_len - num_lines + 1)

        # Compute window of lines
        start_idx = self.offset
        end_idx = start_idx + num_lines

        # Draw lines
        x,y = self.pos
        y -= min(self.offset * line_h, self.pos[1] + 5)
        for line in self.lines[start_idx:end_idx]:
            if line:
                txt_surf = FONT.render(line, True, COLOR_OUT)
                surf.blit(txt_surf, (x, y))
            y += line_h

        # Draw hint
        hint = FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT)
        surf.blit(hint, (surf.get_width() - hint.get_width() - 10, 10))
