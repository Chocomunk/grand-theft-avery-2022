from dis import code_info
import pygame as pg
from gui.labelbox import TXT_H

from shell.env import ENV
from gui.widget import Widget

import math

pg.init()
COLOR_OUT = pg.Color('white')
FONT = pg.font.SysFont('Arial', 16)
TXT_W, TXT_H = FONT.size("O")

class RenderWidget(Widget):

    def __init__(self, on_finish):
        self.finish_cb = on_finish


    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()


    def update(self):
        # TODO: Maybe should do the node children computations in here
        pass


    def get_scr_pos(self, s, n, id):
        x, y = id % n, id // n        # Get position on an nxn grid
        return x * s // n, y * s // n # Scale by screen dimensions


    def draw(self, surf: pg.Surface):
        # NOTE: This is all pretty inefficient but I don't like thinking
        scr_width, scr_height = surf.get_width(), surf.get_height()

        # Get visited nodes and all their children (visible nodes)
        history = ENV.global_history.copy()
        for node in ENV.global_history:
            history |= set(node.children)
        
        nodes = {node.id: node for node in history}
        # Get a square grid to draw nodes on
        n = math.ceil(math.sqrt(max(nodes.keys()) + 1))
        # TODO: Center the whole graph
        # Don't want to draw off the screen
        offset = 200
        s = min(scr_width, scr_height) - offset
        radius = min(s // n, 50)

        for i, (id, node) in enumerate(nodes.items()):
            posx, posy = self.get_scr_pos(s, n, id)
            # Where to draw node
            x, y = posx + offset // 2, posy + offset // 2
            # Draw connections between nodes
            # TODO: Deal with overlapping edges
            for child in node.children:
                if child in history:
                    child_x, child_y = self.get_scr_pos(s, n, child.id)
                    child_x += offset // 2
                    child_y += offset // 2
                    pg.draw.line(surf, (0, 128, 0), (child_x, child_y), (x, y), 5)

                    # Draw direction for edge
                    # TODO: This is pretty weird, probably not the best way to do this

                    # Compute rotation of line
                    rot = math.degrees(math.atan2(child_y - y, x - child_x)) - 90
                    # Size of arrowhead
                    t = 15
                    # Midpoint of line
                    mid_x, mid_y = (x + child_x) // 2, (y + child_y) // 2
                    # Rotate points by 120 degrees to get equilateral triangle
                    point1 = (mid_x + t * math.sin(math.radians(rot)),
                              mid_y + t * math.cos(math.radians(rot)))
                    point2 = (mid_x + t * math.sin(math.radians(rot - 120)),
                              mid_y + t * math.cos(math.radians(rot - 120)))
                    point3 = (mid_x + t * math.sin(math.radians(rot + 120)),
                              mid_y + t * math.cos(math.radians(rot + 120)))
                    # Draw arrowhead
                    pg.draw.polygon(surf, (128, 0, 0), (point1, point2, point3))

            # Draw node
            pg.draw.circle(surf, (0, 128, 0), (x, y), radius)
            name = node.directory.name
            txt_surf = FONT.render(name, True, COLOR_OUT)
            # Offset name
            surf.blit(txt_surf, (x - len(name) * 4, y - 16))

