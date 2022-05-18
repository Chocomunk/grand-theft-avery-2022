import pygame as pg

from shell.env import ENV
from gui.widget import Widget
from gui.constants import Colors, Fonts


COLOR_DIR = Colors.DIR
COLOR_PROG = Colors.PROG
COLOR_FILE = Colors.FILE
FONT = Fonts.TERMINAL


class DirectoryWidget(Widget):

    def __init__(self, pos=(20,20), line_spacing=5, sec_spacing=10):
        self.x, self.y = pos
        self.line_spacing = line_spacing
        self.sec_spacing = sec_spacing

        self.dirs = []
        self.progs = []
        self.files = []

    def handle_event(self, event: pg.event.Event):
        pass

    def update(self):
        if ENV.curr_node:
            self.dirs = ENV.curr_node.list_children()
            self.progs = ENV.curr_node.directory.list_programs()
            self.files = ENV.curr_node.directory.list_files()
        else:
            self.dirs = []
            self.progs = []
            self.files = []

    def draw(self, surf: pg.Surface):
        h = self.y
        w = self.x
        for dir in self.dirs:
            txt_surf = FONT.render(dir, True, COLOR_DIR)
            surf.blit(txt_surf, (w, h))
            h += txt_surf.get_height() + self.line_spacing

        h += self.sec_spacing - self.line_spacing
        for prog in self.progs:
            txt_surf = FONT.render(prog, True, COLOR_PROG)
            surf.blit(txt_surf, (w, h))
            h += txt_surf.get_height() + self.line_spacing

        h += self.sec_spacing - self.line_spacing
        for file in self.files:
            txt_surf = FONT.render(file, True, COLOR_FILE)
            surf.blit(txt_surf, (w, h))
            h += txt_surf.get_height() + self.line_spacing
