import sys
import time
import math
import pygame as pg

from string import ascii_lowercase

from gui.widget import Widget
from gui.view import MainView
from system.program import ExitCode
from system.usrbin_programs import UnlockPassword


# TODO: Clean up color and font handling
pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
COLOR_BOX = pg.Color(15, 15, 15)
COLOR_ACTIVE = pg.Color(80, 80, 80)
FONT = pg.font.SysFont('Consolas', 54)      # Must be a uniform-sized "terminal font"
FONT_HINT = pg.font.SysFont('Consolas', 14)      # Must be a uniform-sized "terminal font"
TXT_W, TXT_H = FONT.size("O")
HNT_H = FONT_HINT.get_height()


SHAKE_DUR = 0.25        # (sec)
SHAKE_DIST = 15         # (px)
SHAKE_SPEED = 16        # (hz / pi)


ALPHABET = ascii_lowercase
ALPH_LEN = len(ascii_lowercase)
ALPH_IND = {c: i for i, c in enumerate(ALPHABET)}


def sub(s, sub_list):
    """ Substitutes characters in a string """
    return "".join([sub_list[ALPH_IND[c]] for c in s])


class UnlockSubPassword(UnlockPassword):

    NAME = "unlock"

    def cli_main(self, args) -> ExitCode:
        out = self.check_node(args)
        if not out:
            return ExitCode.ERROR

        print("`{}` is only available in the GUI!".format(self.NAME), file=sys.stderr)
        
        return ExitCode.OK

    def gui_main(self, gui, args) -> ExitCode:
        out = self.check_node(args)
        if not out:
            return ExitCode.ERROR
        dirname, node = out

        def leave_window(passwd):
            if node.try_password(passwd):
                print("Success! {0} is unlocked.".format(dirname))
            gui.pop_view()
            
        subs = ALPHABET[-1] + ALPHABET[:-1]
        passwd_widg = SubPasswordWidget(node.password, subs, leave_window)
        new_view = MainView(gui.size)
        new_view.add_widget(passwd_widg)
        gui.push_view("subpasswd", new_view)
        return ExitCode.OK


class SubPasswordWidget(Widget):

    def __init__(self, password, sub_list, on_finished, pos=(20,20), spacing=20):
        self.pos = pos
        self.spacing = spacing
        self.finish_cb = on_finished

        self.answer = password
        self.pass_text = sub(password, sub_list)
        self.subs = [c for c in ALPHABET]

        self.anim_time = 0
        self.offset = 0
        self.cursor = 0

        self.box_surf = self.draw_alph_boxes()

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            # Leave
            if event.key == pg.K_ESCAPE:
                self.finish_cb(self.pass_text)

            elif event.key == pg.K_RETURN:
                self.attempt()

            # Move cursor
            elif event.key == pg.K_LEFT:
                self.cursor = max(0, self.cursor - 1)
            elif event.key == pg.K_RIGHT:
                self.cursor = min(ALPH_LEN-1, self.cursor + 1)

            # Type or delete text
            elif event.unicode in ALPH_IND:
                self.subs[self.cursor] = event.unicode

    def update(self):
        t = time.time() - self.anim_time
        if SHAKE_DUR > t:
            self.offset = math.sin(SHAKE_SPEED*t*math.pi) * SHAKE_DIST
        else:
            self.offset = 0

    def attempt(self):
        # Check attempt against answer
        ans = "".join(self.answer.split())
        passwd = sub(self.pass_text, self.subs)
        if passwd == ans:
            self.finish_cb(passwd)
        else:
            self.anim_time = time.time()
            self.text = ""

    # TODO: set padding as constants
    def draw(self, surf: pg.Surface):
        # Draw boxes centered
        cx, cy = surf.get_width() // 2, surf.get_height() // 3   
        bw, bh = self.box_surf.get_size()
        bx, by = cx - bw // 2, 2*cy - bh // 2
        surf.blit(self.box_surf, (bx,by))

        # Draw cipher text
        text = sub(self.pass_text, self.subs)
        txt_surf = FONT.render(text, True, COLOR_OUT)
        tw, th = txt_surf.get_size()
        tx, ty = cx - tw // 2, cy - th // 2
        tx += self.offset
        surf.blit(txt_surf, (tx,ty))

        # Draw substitutions
        self.draw_subs(surf, (bx,by+TXT_H+self.spacing))

        # Draw hint
        surf.blit(FONT_HINT.render("Move with left/right arrows", True, COLOR_OUT), (20,20))
        surf.blit(FONT_HINT.render("Press (enter) to submit", True, COLOR_OUT), (20,25+HNT_H))
        surf.blit(FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT), (20,30+2*HNT_H))

    def draw_alph_boxes(self):
        width = (TXT_W + self.spacing + 20) * ALPH_LEN
        height = 2*TXT_H + self.spacing + 20
        surf = pg.Surface((width, height), pg.SRCALPHA, 32)

        x, y = 0, TXT_H + self.spacing
        for c in ALPHABET:
            surf.blit(FONT.render(c, True, COLOR_OUT), (x+10, 0))
            pg.draw.rect(surf, COLOR_BOX, pg.Rect(x, y, TXT_W + 20, TXT_H + 20))
            x += TXT_W + self.spacing + 20

        return surf

    def draw_subs(self, surf: pg.Surface, pos):
        x, y = pos
        for i in range(ALPH_LEN):
            if i == self.cursor:
                pg.draw.rect(surf, COLOR_ACTIVE, pg.Rect(x, y, TXT_W + 20, TXT_H + 20))
            surf.blit(FONT.render(self.subs[i], True, COLOR_OUT), (x+10, y+10))
            x += TXT_W + self.spacing + 20
