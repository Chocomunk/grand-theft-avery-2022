import math

import pygame as pg
from pygame.gfxdraw import aacircle, filled_circle

from shell.env import ENV
from gui.widget import Widget


pg.init()
COLOR_CURRENT = pg.Color("#EBD288")
COLOR_VISITED = pg.Color("#183078")
COLOR_VISIBLE = pg.Color("#9EAEDE")
COLOR_EDGE = pg.Color("#F1FFFA")
# COLOR_ARROW = pg.Color("#464E47")
COLOR_ARROW = COLOR_EDGE
COLOR_TEXT = COLOR_EDGE
FONT = pg.font.SysFont('Consolas', 18)
TXT_W, TXT_H = FONT.size("O")


# TODO: replace grid with mesh
class RenderWidget(Widget):

    def __init__(self, on_finish, base_r=50, arrow_size=10):
        self.finish_cb = on_finish
        self.base_r = base_r
        self.arrow_size = arrow_size

        # Get visited nodes and all their children (visible nodes)
        self.nodes = ENV.visited_nodes.copy()
        for node in ENV.visited_nodes:
            self.nodes |= set(node.children)

        # TODO: update self.r based on number of nodes.
        self.r = base_r

        # TODO: replace grid with mesh
        # Compute grid dimensions
        max_id = max(n.id for n in self.nodes)
        self.d = math.ceil(math.sqrt(max_id + 1))

        # Compute map surface size. Draw nodes with 2r space between eachother
        w = 4 * self.r * self.d - 2 * self.r + 5
        h = 4 * self.r * (1 + max_id // self.d) - 2 * self.r + 5
        self.surf = pg.Surface((w,h), pg.SRCALPHA, 32)
        self.draw_map()

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()

    def update(self):
        pass

    def draw(self, surf: pg.Surface):
        # Draw map onto parent surface
        w, h = surf.get_size()
        t_w, t_h = self.surf.get_size()
        cx, cy = w // 2, h // 2
        px, py = cx - t_w // 2, cy - t_h // 2
        surf.blit(self.surf, (px, py))

    def get_scr_pos(self, node):
        # Get position on an nxn grid
        x, y = node.id % self.d, node.id // self.d
        return self.r + 4 * x * self.r, self.r + 4 * y * self.r

    def draw_map(self):
        # Draw connections between nodes
        for child in ENV.curr_node.children:
            if child in self.nodes:
                self.draw_line(self.surf, ENV.curr_node, child)
        for par in ENV.curr_node.parents:
            if par in ENV.visited_nodes:
                self.draw_line(self.surf, par, ENV.curr_node)

        # Draw nodes
        for node in self.nodes:
            self.draw_node(self.surf, node)

    def draw_line(self, surf, node1, node2):
        x1, y1 = self.get_scr_pos(node1)
        x2, y2 = self.get_scr_pos(node2)

        # Draw line
        pg.draw.line(surf, COLOR_EDGE, (x2, y2), (x1, y1), 5)

        # Compute angle of line
        rot = math.atan2(y2 - y1, x1 - x2) - math.pi/2
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw direction arrow
        # Rotate points by 120 degrees to get equilateral triangle
        ang = 2 * math.pi / 3
        s = self.arrow_size
        point1 = (mid_x + s * math.sin(rot),
                    mid_y + s * math.cos(rot))
        point2 = (mid_x + s * math.sin(rot - ang),
                    mid_y + s * math.cos(rot - ang))
        point3 = (mid_x + s * math.sin(rot + ang),
                    mid_y + s * math.cos(rot + ang))
        pg.draw.polygon(surf, COLOR_ARROW, (point1, point2, point3))

    def draw_node(self,surf, node):
        x, y = self.get_scr_pos(node)

        # Determine node color
        color = COLOR_VISIBLE                   # Default to 'visible' color
        if node == ENV.curr_node:
            color = COLOR_CURRENT
        elif node in ENV.visited_nodes:
            color = COLOR_VISITED

        # Draw node
        aacircle(surf, x, y, self.r, color)
        filled_circle(surf, x, y, self.r, color)
        name = node.directory.name
        txt_surf = FONT.render(name, True, COLOR_TEXT)

        # Center and render name
        w, h = txt_surf.get_size()
        surf.blit(txt_surf, (x - w//2, y - h//2))
