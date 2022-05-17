import time
import math
import pygame as pg

from gui.widget import Widget


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
FONT = pg.font.SysFont('Consolas', 54)      # Must be a uniform-sized "terminal font"
FONT_HINT = pg.font.SysFont('Consolas', 14)      # Must be a uniform-sized "terminal font"
TXT_W, TXT_H = FONT.size("O")


class PasswordWidget(Widget):

    def __init__(self, password, on_finished, pos=(20,20), spacing=20):
        self.pos = pos
        self.spacing = spacing
        self.finish_cb = on_finished

        self.answer = password
        self.text = ""
        self.active = False         # Should be enabled by creator
        self.anim_time = 0
        self.offset = 0

        self.box_surf = self.draw_boxes()

    def handle_event(self, event: pg.event.Event):
        if self.active:
            if event.type == pg.KEYDOWN:
                # Leave
                if event.key == pg.K_ESCAPE:
                    self.finish_cb(self.text)

                # Type or delete text
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif not event.key == pg.K_RETURN:
                    self.text += event.unicode

    def update(self):
        # Compute offset
        t = time.time() - self.anim_time
        if 0.25 > t:
            self.offset = math.sin(t*8*math.pi) * 50
        else:
            self.offset = 0

        # Check if password is cleared
        if not self.answer:
            self.finish_cb("")
            return

        # Check attempt against answer
        ans = "".join(self.answer.split())
        ans_len = len(ans)
        if len(self.text) >= ans_len:
            if self.text[:ans_len] == ans:
                # TODO: finish anim
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
        surf.blit(FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT), (20,20))

    def draw_boxes(self):
        width = (TXT_W + self.spacing + 20) * len(self.answer)
        height = TXT_H + 20
        box_surf = pg.Surface((width, height), pg.SRCALPHA, 32)

        x = 0
        for c in self.answer:
            if c != " ":
                pg.draw.rect(box_surf, (15, 15, 15), 
                            pg.Rect(x, 0, TXT_W + 20, height))
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
