import math

import pygame as pg

from shell.env import ENV
from gui.widget import Widget


pg.init()
COLOR_OUT = pg.Color('white')
FONT = pg.font.SysFont('Arial', 16)
TXT_W, TXT_H = FONT.size("O")


# TODO: replace grid with mesh
class RenderWidget(Widget):

    def __init__(self, on_finish, base_r=50):
        self.finish_cb = on_finish
        self.base_r = base_r

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
        w = 4 * self.r * self.d - 2 * self.r
        h = 4 * self.r * (1 + max_id // self.d) - 2 * self.r
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
        pg.draw.line(surf, (0, 128, 0), (x2, y2), (x1, y1), 5)

        # Compute angle of line
        rot = math.atan2(y2 - y1, x1 - x2) - math.pi/2
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw direction arrow
        # Rotate points by 120 degrees to get equilateral triangle
        arrow_size = 15
        ang = 2 * math.pi / 3
        point1 = (mid_x + arrow_size * math.sin(rot),
                    mid_y + arrow_size * math.cos(rot))
        point2 = (mid_x + arrow_size * math.sin(rot - ang),
                    mid_y + arrow_size * math.cos(rot - ang))
        point3 = (mid_x + arrow_size * math.sin(rot + ang),
                    mid_y + arrow_size * math.cos(rot + ang))
        pg.draw.polygon(surf, (128, 0, 0), (point1, point2, point3))

    def draw_node(self,surf, node):
        x, y = self.get_scr_pos(node)

        # Draw node
        pg.draw.circle(surf, (0, 128, 0), (x, y), self.r)
        name = node.directory.name
        txt_surf = FONT.render(name, True, COLOR_OUT)

        # Center and render name
        w, h = txt_surf.get_size()
        surf.blit(txt_surf, (x - w//2, y - h//2))
