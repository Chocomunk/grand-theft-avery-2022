import pygame as pg
from pygame import Surface

from typing import List
from gui.widget import Widget


# NOTE: You can put views inside other views


# TODO: Maybe look into using Rects? Other people use it but im not sure how
#       useful it is.
class MainView(Widget):

    def __init__(self, size, pos=(0,0), bg_color=(0,0,0,0)):
        self.w, self.h = size
        self.pos = pos
        self.bg_color = bg_color

        self.surf = Surface((self.w, self.h), pg.SRCALPHA, 32)
        self.widgets: List[Widget] = []

    def add_widget(self, widget: Widget):
        self.widgets.append(widget)

    def handle_event(self, event: pg.event.Event):
        for widget in self.widgets:
            widget.handle_event(event)

    def update(self):
        for widget in self.widgets:
            widget.update()

    def draw(self, surf: Surface):
        self.surf.fill(self.bg_color)
        for widget in self.widgets:
            widget.draw(self.surf)
        surf.blit(self.surf, self.pos)


class SplitView(Widget):

    def __init__(self, widg1: Widget, widg2: Widget, 
                    size, pos=(0,0), weight=0.5, horizontal=False,
                    bg_color1=(0,0,0,0), bg_color2=(0,0,0,0)):
        w, h = size
        self.w, self.h = w, h
        self.x, self.y = pos
        self.weight = weight
        self.horizontal = horizontal
        self.bg_color1 = bg_color1
        self.bg_color2 = bg_color2

        if horizontal:
            self.t = int(h*weight)      # Var to store surf1 height
            self.surf1 = Surface((w, self.t), pg.SRCALPHA, 32)
            self.surf2 = Surface((w, self.t), pg.SRCALPHA, 32)
        else:
            self.t = int(w*weight)      # Var to store surf1 width
            self.surf1 = Surface((self.t, h), pg.SRCALPHA, 32)
            self.surf2 = Surface((self.t, h), pg.SRCALPHA, 32)

        self.widg1 = widg1
        self.widg2 = widg2

    def handle_event(self, event: pg.event.Event):
        if self.widg1:
            self.widg1.handle_event(event)
        if self.widg2:
            self.widg2.handle_event(event)

    def update(self):
        if self.widg1:
            self.widg1.update()
        if self.widg2:
            self.widg2.update()

    def draw(self, surf: Surface):
        self.surf1.fill(self.bg_color1)
        self.surf2.fill(self.bg_color2)

        if self.widg1:
            self.widg1.draw(self.surf1)
        if self.widg2:
            self.widg2.draw(self.surf2)

        if self.horizontal:
            surf.blit(self.surf1, (self.x, self.y))
            surf.blit(self.surf2, (self.x, self.y + self.t + 1))
        else:
            surf.blit(self.surf1, (self.x, self.y))
            surf.blit(self.surf2, (self.x + self.t + 1, self.y))
