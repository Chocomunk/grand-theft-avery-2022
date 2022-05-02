from enum import Enum
from pygame import Surface
from pygame.event import Event
from abc import ABC, abstractmethod


class WidgetStatus(Enum):
    OK=0
    EXIT=-1


class Widget(ABC):

    @abstractmethod
    def handle_event(self, event: Event) -> WidgetStatus:
        pass

    @abstractmethod
    def update(self) -> WidgetStatus:
        pass

    @abstractmethod
    def draw(self, surf: Surface):
        pass
