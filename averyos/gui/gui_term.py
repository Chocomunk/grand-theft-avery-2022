from io import StringIO
import sys
import pygcurse
import pygame as pg
from pygame import Surface


# self.curse = pygcurse.PygcurseSurface(font=pygame.font.SysFont('arial', 18), windowsurface=self.win)

pg.init()
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.SysFont('Consolas', 14)


class TerminalGUI:

    def __init__(self, x, y, w, h, text='', prompt_func=lambda: ""):
        self.file = StringIO()
        self.prompt_func = prompt_func
        self.text = text
        self.active = False
        self.input_cbs = []

        self.file.write(self.prompt_func())

        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.txt_surface = FONT.render("", True, self.color)

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.file.write(self.text + '\n')
                    for cb in self.input_cbs:
                        if not cb(self.text):
                            return False
                    self.file.write(self.prompt_func())
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
        return True

    def update(self):
        # Resize the box if the text is too long.
        self.render_text()
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, parent_surf: Surface):
        parent_surf.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # pg.draw.rect(parent_surf, self.color, self.rect, 2)

    def add_input_listener(self, func):
        self.input_cbs.append(func)

    def render_text(self):
        full_text = self.file.getvalue() + self.text
        full_text = full_text.replace('\t', "    ")
        # print(repr(full_text), file=sys.__stdout__)
        lines = full_text.split('\n')

        height = 0
        max_width = 0
        surfs = []
        for line in lines:
            surf = FONT.render(line, True, self.color)
            height += surf.get_height() + 5
            max_width = max(max_width, surf.get_width())
            surfs.append(surf)
        self.txt_surface = Surface((max_width, height), pg.SRCALPHA, 32)

        height = 0
        for surf in surfs:
            self.txt_surface.blit(surf, (0, height))
            height += surf.get_height() + 5


class AveryOSWin:

    def __init__(self) -> None:
        self.win = pg.display.set_mode((640,480))
        self.elements = []

    def update(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    return False
            for el in self.elements:
                if el.handle_event(event) is False:
                    return False

        for el in self.elements:
            el.update()

        return True

    def render(self):
        self.win.fill((30, 30, 30))
        for el in self.elements:
            el.draw(self.win)
