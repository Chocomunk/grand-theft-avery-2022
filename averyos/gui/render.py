import sys
import math

import pygame as pg
from pygame.gfxdraw import aacircle, filled_circle

from shell.env import ENV
from gui.widget import Widget


pg.init()
COLOR_CURRENT = pg.Color("#EBD288")
COLOR_VISITED = pg.Color("#183078")
COLOR_VISIBLE = pg.Color("#9EAEDE")
COLOR_INVISIBLE = pg.Color("#525663")
COLOR_EDGE = pg.Color("#F1FFFA")
# COLOR_ARROW = pg.Color("#464E47")
COLOR_ARROW = COLOR_EDGE
COLOR_TEXT = COLOR_EDGE
FONT = pg.font.SysFont('Consolas', 18)
TXT_W, TXT_H = FONT.size("O")


# TODO: replace grid with mesh
class RenderWidget(Widget):

    def __init__(self, on_finish, nodes=None, base_r=50, arrow_size=10):
        self.finish_cb = on_finish
        self.base_r = base_r
        self.r = self.base_r
        self.arrow_size = arrow_size

        self.l = 0
        self.t = 0

        # Get visited nodes and all their children (visible nodes)
        self.visible = ENV.visited_nodes.copy()
        for node in ENV.visited_nodes:
            self.visible |= set(node.children)
        self.nodes = self.visible if not nodes else nodes

        # Initialize the surface and draw the map
        w, h = self.update_dims()
        self.map_surf = pg.Surface((w,h), pg.SRCALPHA, 32)
        self.draw_map(self.map_surf)

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()

    # TODO: Update when chanding directory
    def update(self):
        pass

    def draw(self, surf: pg.Surface):
        # Draw map onto parent surface (centered)
        w, h = surf.get_size()
        m_w, m_h = self.map_surf.get_size()
        cx, cy = w // 2, h // 2
        px, py = cx - m_w // 2, cy - m_h // 2
        surf.blit(self.map_surf, (px, py))

    # TODO: replace grid with mesh
    def get_scr_pos(self, node):
        if ENV.mesh:
            if node.id < len(ENV.mesh.points):
                x, y = ENV.mesh.points[node.id]
                return self.r + int(x) - self.l, self.r + int(y) - self.t
        else:
            rel_id = node.id - min(n.id for n in self.nodes)    # Relative id

            # Get position on an nxn grid
            x, y = rel_id % self.d, rel_id // self.d
            return self.r + 4 * x * self.r, self.r + 4 * y * self.r

    def update_dims(self):
        # TODO: update self.r based on number of nodes.
        self.r = self.base_r

        # Compute grid dimensions
        ids = [n.id for n in self.nodes]
        self.d = math.ceil(math.sqrt(max(ids) - min(ids) + 1))

        if ENV.mesh:
            self.l, self.t, w, h = [int(x) for x in ENV.mesh.node_dims(self.nodes)]
            w, h = w + self.r, h + self.r
        else:
            w = 0
            h = 0
            # Find max width/height
            for node in self.nodes:
                w1, h1 = self.get_scr_pos(node)
                w = max(w, w1)
                h = max(h, h1)

        return w + self.r + 5, h + self.r + 5

    def draw_map(self, surf):
        # Draw connections between nodes
        for child in ENV.curr_node.children:
            if child in self.nodes:
                self.draw_line(surf, ENV.curr_node, child)
        for par in ENV.curr_node.parents:
            if par in ENV.visited_nodes:
                self.draw_line(surf, par, ENV.curr_node)

        # Draw nodes
        for node in self.nodes:
            self.draw_node(surf, node)

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
        if node == ENV.curr_node:
            color = COLOR_CURRENT
        elif node in ENV.visited_nodes:
            color = COLOR_VISITED
        elif node in self.visible:
            color = COLOR_VISIBLE
        else:
            color = COLOR_INVISIBLE             # Default to 'invisible' color

        # Draw node
        aacircle(surf, x, y, self.r, color)
        filled_circle(surf, x, y, self.r, color)

        # Center and render name
        if color != COLOR_INVISIBLE:
            name = node.directory.name
            txt_surf = FONT.render(name, True, COLOR_TEXT)
            w, h = txt_surf.get_size()
            surf.blit(txt_surf, (x - w//2, y - h//2))
