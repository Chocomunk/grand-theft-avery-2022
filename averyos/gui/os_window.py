import pygame as pg


class OSWindow:

    def __init__(self, size) -> None:
        self.win = pg.display.set_mode(size)
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