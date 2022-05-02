import pygame as pg
from enum import Enum
from pygame import Surface
from abc import ABC, abstractmethod


class WidgetStatus(Enum):
    OK=0
    EXIT=1


class Widget(ABC):

    @abstractmethod
    def handle_event(self, event: pg.event.Event) -> WidgetStatus:
        pass

    @abstractmethod
    def update(self) -> WidgetStatus:
        pass

    @abstractmethod
    def draw(self, surf: Surface):
        pass
