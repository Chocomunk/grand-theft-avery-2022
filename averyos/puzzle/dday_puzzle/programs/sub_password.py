import sys
import time
import math
import pygame as pg

from string import ascii_lowercase

from shell.env import ENV
from gui.widget import Widget
from gui.view import MainView
from gui.constants import Colors, Fonts

from system.program import ExitCode
from system.usrbin_programs import UnlockPassword


COLOR_OUT = Colors.TXT_OUT
COLOR_BOX = Colors.PASS_BOX
COLOR_ACTIVE = Colors.CURSOR

FONT_CIPH = Fonts.PROMPT
FONT_PASS = Fonts.PASSWORD
FONT_HINT = Fonts.HINT
CIPH_W, CIPH_H = FONT_CIPH.size("O")
PASS_W, PASS_H = FONT_PASS.size("O")
HINT_H = FONT_HINT.get_height()


SHAKE_DUR = 0.25        # (sec)
SHAKE_DIST = 15         # (px)
SHAKE_SPEED = 16        # (hz / pi)


ALPHABET = ascii_lowercase
ALPH_LEN = len(ascii_lowercase)
ALPH_IND = {c: i for i, c in enumerate(ALPHABET)}


def sub(s, sub_list):
    """ Substitutes characters in a string """
    return "".join([sub_list[ALPH_IND[c]] if c in ALPH_IND else c 
                    for c in s])


class UnlockSubPassword(UnlockPassword):

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

        filename = node.directory.name.lower() + "-cipher.txt"
        if not filename in ENV.curr_node.directory.files:
            print("No cipher text file found for node {0}".format(
                    node.directory.name), file=sys.stderr)
            return ExitCode.ERROR
        cipher_file = ENV.curr_node.directory.files[filename]

        def leave_window(passwd):
            if node.try_password(passwd):
                print("Success! {0} is unlocked.".format(dirname))
            gui.pop_view()
            
        cipher_text = cipher_file.get_data().lower()
        subs = node.password
        passwd_widg = SubPasswordWidget(cipher_text, subs, leave_window)
        new_view = MainView(gui.size)
        new_view.add_widget(passwd_widg)
        gui.push_view("subpasswd", new_view)
        return ExitCode.OK


class SubPasswordWidget(Widget):

    def __init__(self, cipher_text, sub_list, on_finished, pos=(20,20), spacing=20):
        self.pos = pos
        self.spacing = spacing
        self.finish_cb = on_finished

        self.sub_ans = "".join([c for c in sub_list])
        self.subs = [c for c in ALPHABET]
        self.cipher_text = cipher_text.split('\n')

        self.text_w = max(len(l) for l in self.cipher_text) * CIPH_W
        self.text_h = len(self.cipher_text) * (CIPH_H + 5)

        self.anim_time = 0
        self.offset = 0
        self.cursor = 0

        self.box_surf = self.draw_alph_boxes()

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            # Leave
            if event.key == pg.K_ESCAPE:
                self.finish_cb("")

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
        sub_txt = "".join(self.subs)
        if sub_txt == self.sub_ans:
            self.finish_cb(sub_txt)
        else:
            self.anim_time = time.time()
            self.text = ""

    # TODO: set padding as constants
    def draw(self, surf: pg.Surface):
        # Draw boxes centered
        cx, cy = surf.get_width() // 2, surf.get_height() // 3   

        # Draw cipher text at h/3
        tx, ty = cx - self.text_w // 2, cy - self.text_h // 2
        tx += self.offset
        self.draw_cipher(surf, (tx, ty))

        # Draw boxes at h * (2/3)
        bw, bh = self.box_surf.get_size()
        bx, by = cx - bw // 2, 2*cy - bh // 2
        surf.blit(self.box_surf, (bx,by))

        # Draw substitutions
        self.draw_subs(surf, (bx,by+PASS_H+self.spacing))

        # Draw hint
        surf.blit(FONT_HINT.render("Move with left/right arrows", True, COLOR_OUT), (20,20))
        surf.blit(FONT_HINT.render("Press (enter) to submit", True, COLOR_OUT), (20,25+HINT_H))
        surf.blit(FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT), (20,30+2*HINT_H))

    def draw_alph_boxes(self):
        width = (PASS_W + self.spacing + 20) * ALPH_LEN
        height = 2*PASS_H + self.spacing + 20
        surf = pg.Surface((width, height), pg.SRCALPHA, 32)

        x, y = 0, PASS_H + self.spacing
        for c in ALPHABET:
            surf.blit(FONT_PASS.render(c, True, COLOR_OUT), (x+10, 0))
            pg.draw.rect(surf, COLOR_BOX, pg.Rect(x, y, PASS_W + 20, PASS_H + 20))
            x += PASS_W + self.spacing + 20

        return surf

    def draw_subs(self, surf: pg.Surface, pos):
        x, y = pos
        for i in range(ALPH_LEN):
            if i == self.cursor:
                pg.draw.rect(surf, COLOR_ACTIVE, pg.Rect(x, y, PASS_W + 20, PASS_H + 20))
            surf.blit(FONT_PASS.render(self.subs[i], True, COLOR_OUT), (x+10, y+10))
            x += PASS_W + self.spacing + 20

    def draw_cipher(self, surf: pg.Surface, pos):
        x, y = pos
        for line in self.cipher_text:
            text = sub(line, self.subs)
            surf.blit(FONT_CIPH.render(text, True, COLOR_OUT), (x,y))
            y += CIPH_H + 5
