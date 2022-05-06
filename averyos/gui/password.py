import sys
import pygame as pg

from gui.widget import Widget


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
FONT = pg.font.SysFont('Consolas', 54)      # Must be a uniform-sized "terminal font"
FONT_HINT = pg.font.SysFont('Consolas', 14)      # Must be a uniform-sized "terminal font"


class PasswordWidget(Widget):

    def __init__(self, password, on_finished, pos=(20,20), spacing=20):
        self.pos = pos
        self.spacing = spacing
        self.finish_cb = on_finished

        self.answer = password
        self.text = ""
        self.active = False         # Should be enabled by creator

    def handle_event(self, event: pg.event.Event):
        if self.active:
            if event.type == pg.KEYDOWN:
                # Leave
                if event.key == pg.K_ESCAPE:
                    self.finish_cb(self.text)

                # Type or delete text
                if event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    # TODO: no pwd/fail/success animations
    def update(self):
        if not self.answer:
            self.text = "NOPE"
            self.answer = ""
            return

        ans_len = len(self.answer)
        if len(self.text) >= ans_len:
            if self.text[:ans_len] == self.answer:
                # TODO: finish
                self.finish_cb(self.text)
            else:
                self.text = ""

    # TODO: figure out sizes before-hand
    # TODO: set padding as constants
    def draw(self, surf: pg.Surface):
        surfs = []
        width = 0
        height = 0
        for c in self.answer:
            txt_surf = FONT.render(c, True, COLOR_OUT)
            width += txt_surf.get_width() + self.spacing + 20
            height = max(height, txt_surf.get_height() + 20)
            surfs.append(txt_surf)

        tmp_surf = pg.Surface((width, height), pg.SRCALPHA, 32)
        x, y = 0, 0
        for i, txt_surf in enumerate(surfs):
            pg.draw.rect(tmp_surf, (15, 15, 15), 
                        pg.Rect(x, y, txt_surf.get_width() + 20, height))
            if i < len(self.text):
                usr_txt = FONT.render(self.text[i], True, COLOR_OUT)
                tmp_surf.blit(usr_txt, (x+10, y+10))
            x += txt_surf.get_width() + self.spacing + 20

        cx, cy = surf.get_width() // 2, surf.get_height() // 2       
        px, py = cx - width // 2, cy - height // 2
        surf.blit(tmp_surf, (px, py))

        surf.blit(FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT), (20,20))
