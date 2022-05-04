import sys
import pygame as pg

from gui.widget import Widget


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
FONT = pg.font.SysFont('Consolas', 48)      # Must be a uniform-sized "terminal font"


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
                    self.finish_cb()

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

        if len(self.text) == len(self.answer):
            if self.text == self.answer:
                # TODO: finish
                self.finish_cb()
            else:
                self.text = ""

    # TODO: figure out sizes before-hand
    def draw(self, surf: pg.Surface):
        surfs = []
        width = 0
        height = 0
        for c in self.answer:
            txt_surf = FONT.render(c, True, COLOR_OUT)
            width += txt_surf.get_width() + self.spacing
            height = max(height, txt_surf.get_height())
            surfs.append(txt_surf)

        tmp_surf = pg.Surface((width, height), pg.SRCALPHA, 32)
        x, y = 0, 0
        for i, txt_surf in enumerate(surfs):
            pg.draw.rect(tmp_surf, (0, 0, 0), 
                        pg.Rect(x, y, txt_surf.get_width(), height))
            if i < len(self.text):
                usr_txt = FONT.render(self.text[i], True, COLOR_OUT)
                tmp_surf.blit(usr_txt, (x, y))
            x += txt_surf.get_width() + self.spacing

        cx, cy = surf.get_width() // 2, surf.get_height() // 2       
        px, py = cx - width // 2, cy - height // 2
        surf.blit(tmp_surf, (px, py))

        surf.blit(FONT.render("Press (esc) to exit...", True, COLOR_OUT), (20,20))
