import pygame as pg
from abc import ABC, abstractmethod


class Widget(ABC):

    @abstractmethod
    def handle_event(self, event: pg.event.Event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def draw(self, surf: pg.Surface):
        pass
