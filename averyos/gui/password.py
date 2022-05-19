import time
import math
import pygame as pg

from string import ascii_letters

from gui.widget import Widget
from gui.constants import Colors, Fonts


COLOR_OUT = Colors.TXT_OUT
COLOR_BOX = Colors.PASS_BOX
FONT = Fonts.PASSWORD
FONT_HINT = Fonts.HINT
TXT_W, TXT_H = FONT.size("O")
HNT_H = FONT_HINT.get_height()

SHAKE_DUR = 0.25        # (sec)
SHAKE_DIST = 15         # (px)
SHAKE_SPEED = 16        # (hz / pi)


class PasswordWidget(Widget):

    def __init__(self, password, on_finished, pos=(20,20), spacing=20):
        self.pos = pos
        self.spacing = spacing
        self.finish_cb = on_finished

        self.answer = password
        self.text = ""
        self.anim_time = 0
        self.offset = 0

        self.box_surf = self.draw_boxes()

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            # Leave
            if event.key == pg.K_ESCAPE:
                self.finish_cb("")

            elif event.key == pg.K_RETURN:
                self.attempt()

            # Type or delete text
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            # elif event.key != pg.K_SPACE:
            elif event.unicode in ascii_letters:
                if len(self.text) < len(self.answer):
                    self.text += event.unicode

    def update(self):
        # Compute offset
        t = time.time() - self.anim_time
        if SHAKE_DUR > t:
            self.offset = math.sin(SHAKE_SPEED*t*math.pi) * SHAKE_DIST
        else:
            self.offset = 0

    def attempt(self):
        # Check attempt against answer
        ans = "".join(self.answer.split())
        if self.text[:len(ans)].lower() == ans.lower():
            self.finish_cb(self.text)
        else:
            self.anim_time = time.time()
            self.text = ""

    # TODO: set padding as constants
    def draw(self, surf: pg.Surface):
        # Draw boxes centered
        cx, cy = surf.get_width() // 2, surf.get_height() // 2
        bw, bh = self.box_surf.get_size()
        px, py = cx - bw // 2, cy - bh // 2
        x, y = px + self.offset, py
        surf.blit(self.box_surf, (x,y))

        # Draw text
        self.draw_text(surf, (x,y))

        # Draw hint
        surf.blit(FONT_HINT.render("Press (enter) to submit", True, COLOR_OUT), (20,20))
        surf.blit(FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT), (20,25+HNT_H))

    def draw_boxes(self):
        width = (TXT_W + self.spacing + 20) * len(self.answer)
        height = TXT_H + 20
        box_surf = pg.Surface((width, height), pg.SRCALPHA, 32)

        x = 0
        for c in self.answer:
            if c != " ":
                pg.draw.rect(box_surf, COLOR_BOX, pg.Rect(x, 0, TXT_W + 20, height))
            x += TXT_W + self.spacing + 20

        return box_surf

    def draw_text(self, surf: pg.Surface, pos):
        x, y = pos
        i = 0
        for c in self.text:
            if self.answer[i] == " ":
                x += TXT_W + self.spacing + 20
            while self.answer[i] == " ":
                i += 1
            surf.blit(FONT.render(c, True, COLOR_OUT), (x+10, y+10))
            x += TXT_W + self.spacing + 20
            i += 1
