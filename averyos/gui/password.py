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
        t = time.time() - self.anim_time
        if 0.25 > t:
            self.offset = math.sin(t*8*math.pi) * 50
        else:
            self.offset = 0

        if not self.answer:
            self.finish_cb("")
            return

        ans = "".join(self.answer.split())
        ans_len = len(ans)
        if len(self.text) >= ans_len:
            if self.text[:ans_len] == ans:
                # TODO: finish anim
                self.finish_cb(self.text)
            else:
                self.anim_time = time.time()
                self.text = ""


    # TODO: figure out sizes before-hand
    # TODO: set padding as constants
    def draw(self, surf: pg.Surface):
        surfs = []
        width = 0
        height = TXT_H + 20
        for c in self.answer:
            width += TXT_W + self.spacing + 20
            # height = max(height, txt_surf.get_height() + 20)
            if c != " ":
                txt_surf = FONT.render(c, True, COLOR_OUT)
                surfs.append(txt_surf)
            else:
                surfs.append(None)

        tmp_surf = pg.Surface((width, height), pg.SRCALPHA, 32)
        x, y = 0, 0
        i = 0
        for txt_surf in surfs:
            if txt_surf:
                pg.draw.rect(tmp_surf, (15, 15, 15), 
                            pg.Rect(x, y, txt_surf.get_width() + 20, height))
                if i < len(self.text):
                    usr_txt = FONT.render(self.text[i], True, COLOR_OUT)
                    tmp_surf.blit(usr_txt, (x+10, y+10))
                i += 1
            x += TXT_W + self.spacing + 20

        cx, cy = surf.get_width() // 2, surf.get_height() // 2       
        px, py = cx - width // 2, cy - height // 2
        surf.blit(tmp_surf, (px + self.offset, py))

        surf.blit(FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT), (20,20))
