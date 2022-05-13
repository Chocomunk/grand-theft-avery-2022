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


class RenderWidget(Widget):

    def __init__(self, size, on_finish, nodes=None, arrow_size=10):
        self.finish_cb = on_finish
        self.arrow_size = arrow_size

        self.l = 0
        self.t = 0

        # Get visited nodes and all their children (visible nodes)
        self.visible = ENV.visited_nodes.copy()
        for node in ENV.visited_nodes:
            self.visible |= set(node.children)
        self.nodes = self.visible if not nodes else nodes

        # Initialize the surface and draw the map
        w, h = ENV.plotter.set_scale(self.nodes, size=size)
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
        x1, y1 = ENV.plotter.get_pos(node1)
        x2, y2 = ENV.plotter.get_pos(node2)

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
        x, y = ENV.plotter.get_pos(node)

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
        aacircle(surf, x, y, ENV.plotter.r, color)
        filled_circle(surf, x, y, ENV.plotter.r, color)

        # Center and render name
        if color != COLOR_INVISIBLE:
            name = node.directory.name
            txt_surf = FONT.render(name, True, COLOR_TEXT)
            w, h = txt_surf.get_size()
            surf.blit(txt_surf, (x - w//2, y - h//2))
