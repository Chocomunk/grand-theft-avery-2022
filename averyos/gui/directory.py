import pygame as pg

from shell.env import ENV
from gui.widget import Widget
from gui.constants import Colors, Fonts


COLOR_DIR = Colors.DIR
COLOR_PROG = Colors.PROG
COLOR_FILE = Colors.FILE
FONT = Fonts.TEXT


DIR_BASE = "gui/assets/"
IMG_SIZE = FONT.get_height()
PADDING = 10


class DirectoryWidget(Widget):

    def __init__(self, pos=(30,30), line_spacing=7, sec_spacing=20):
        self.x, self.y = pos
        self.line_spacing = line_spacing
        self.sec_spacing = sec_spacing

        self.last_node = None

        self.children = []
        self.files = []
        self.progs = []

        self.dir_img = pg.transform.smoothscale(
                            pg.image.load(DIR_BASE+"folder.png"),
                            size=(IMG_SIZE,IMG_SIZE))
        self.file_img = pg.transform.smoothscale(
                            pg.image.load(DIR_BASE+"file.png"),
                            size=(IMG_SIZE,IMG_SIZE))
        self.prog_img = pg.transform.smoothscale(
                            pg.image.load(DIR_BASE+"gear.png"),
                            size=(IMG_SIZE,IMG_SIZE))
        self.lock_img = pg.transform.smoothscale(
                            pg.image.load(DIR_BASE+"locked.png"),
                            size=(IMG_SIZE,IMG_SIZE))

    def handle_event(self, event: pg.event.Event):
        pass

    def update(self):
        if ENV.curr_node is not self.last_node:
            self.children = ENV.curr_node.list_children()
            self.files = ENV.curr_node.directory.list_files()
            self.progs = set(ENV.curr_node.directory.list_programs())

            # View all visible, callable programs.
            self.progs.update({p.NAME for p in ENV.visible_progs})

            self.last_node = ENV.curr_node

    def draw(self, surf: pg.Surface):
        h = self.y
        w = self.x
        for child in self.children:
            txt_surf = FONT.render(child.directory.name, True, COLOR_DIR)
            if child.locked():
                surf.blit(self.lock_img, (w, h))
            else:
                surf.blit(self.dir_img, (w, h))
            surf.blit(txt_surf, (w+IMG_SIZE+PADDING, h))
            h += txt_surf.get_height() + self.line_spacing

        h += self.sec_spacing - self.line_spacing
        for file in self.files:
            txt_surf = FONT.render(file, True, COLOR_FILE)
            surf.blit(self.file_img, (w, h))
            surf.blit(txt_surf, (w+IMG_SIZE+PADDING, h))
            h += txt_surf.get_height() + self.line_spacing

        h += self.sec_spacing - self.line_spacing
        for prog in self.progs:
            txt_surf = FONT.render(prog, True, COLOR_PROG)
            surf.blit(self.prog_img, (w, h))
            surf.blit(txt_surf, (w+IMG_SIZE+PADDING, h))
            h += txt_surf.get_height() + self.line_spacing
