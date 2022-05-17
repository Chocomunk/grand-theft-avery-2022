import io
import sys
import pygame as pg

from PIL import Image
from typing import Dict, Tuple
from collections import Counter
from string import ascii_lowercase

import matplotlib.pyplot as plt

from gui.widget import Widget
from gui.view import MainView
from system.filesystem import File
from system.path_utils import get_file
from system.program import ProgramBase, ExitCode


pg.init()
COLOR_OUT = pg.Color('lightskyblue3')
FONT = pg.font.SysFont('Consolas', 16)      # Must be a uniform-sized "terminal font"
FONT_HINT = pg.font.SysFont('Consolas', 14)      # Must be a uniform-sized "terminal font"
TXT_W, TXT_H = FONT.size("O")


def plot_hist(counts: Dict, size, title: str) -> Tuple[Image.Image, io.BytesIO]:
    fig = plt.figure(figsize=size)
    ix, iy = size[0] / fig.dpi, size[1] / fig.dpi
    fig.set_size_inches((ix,iy))

    plt.bar(list(counts.keys()), list(counts.values()))
    plt.ylabel("Counts")
    plt.title(title)

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    image = Image.open(buffer)
    return image, buffer


class Histogram(ProgramBase):

    NAME = "count"

    def parse_file(self, args) -> File | None:
        if len(args) != 2:
            print("Error: {0} only accepts 1 argument!".format(self.NAME), 
                file=sys.stderr)
            return None
        return get_file(args[1])

    def cli_main(self, args) -> ExitCode:
        file = self.parse_file(args)
        if not file:
            return ExitCode.ERROR

        print("`{}` is only available in the GUI!".format(self.NAME), file=sys.stderr)

        return ExitCode.OK

    def gui_main(self, gui, args) -> ExitCode:
        file = self.parse_file(args)
        if not file :
            return ExitCode.ERROR
            
        if file.is_image:
            print("Error: could not read characters in {0}".format(file.name), file=sys.stderr)
            return ExitCode.ERROR

        counter = Counter(file.get_data().lower())          # Doesn't count defaults
        counts = {c: counter[c] for c in ascii_lowercase}   # Include defaults
        title = "Character counts in {0}".format(file.name)

        # Just replace right-pane, leave directory view in left-pane
        if gui.viewtag == "nav":
            def return_terminal():
                gui.view.widg2 = gui.terminal
            label_widg = HistogramWidget(counts, return_terminal, title=title)
            gui.view.widg2 = label_widg

        # Make a new view.
        else:
            label_widg = HistogramWidget(counts, lambda: gui.pop_view(), title=title)
            new_view = MainView(gui.size)
            new_view.add_widget(label_widg)
            gui.push_view("viewhist", new_view)

        return ExitCode.OK


class HistogramWidget(Widget):

    def __init__(self, counts, on_finish, size=(1280,720), title=""):
        self.finish_cb = on_finish
        img, buf = plot_hist(counts, size, title)
        self.hist_img = pg.image.fromstring(img.tobytes(), img.size, img.mode)
        buf.close()

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()

    def update(self):
        pass

    def draw(self, surf: pg.Surface):
        w, h = surf.get_size()
        iw, ih = self.hist_img.get_size()
        cx, cy = w // 2, h // 2
        ix, iy = cx - iw//2, cy - ih//2

        surf.blit(self.hist_img, (ix,iy))

        hint = FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT)
        surf.blit(hint, (w - hint.get_width() - 10, 10))