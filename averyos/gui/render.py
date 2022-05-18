import math

import pygame as pg
from pygame.gfxdraw import aacircle, filled_circle, aapolygon, filled_polygon

from shell.env import ENV
from gui.widget import Widget
from gui.constants import Colors, Fonts


COLOR_CURRENT = Colors.CURR_NODE
COLOR_VISITED = Colors.VISITED
COLOR_VISIBLE = Colors.VISIBLE
COLOR_INVISIBLE = Colors.INVISIBLE
COLOR_EDGE = Colors.EDGE
COLOR_ARROW = Colors.ARROW
COLOR_TEXT = COLOR_EDGE
COLOR_OUT = Colors.TXT_OUT

FONT = Fonts.NODE_LABEL
FONT_HINT = Fonts.HINT
TXT_W, TXT_H = FONT.size("O")


PADDING = 20
PAN_SPEED = 30
SCALE_SPEED = 0.05
MIN_SCALE = 0.25
MAX_SCALE = 3


class RenderWidget(Widget):

    def __init__(self, size, on_finish, nodes=None, arrow_size=10):
        self.finish_cb = on_finish
        self.arrow_size = arrow_size
        self.offx = 0
        self.offy = 0

        # Get visited nodes and all their children (visible nodes)
        self.visible = ENV.visited_nodes.copy()
        for node in ENV.visited_nodes:
            self.visible |= set(node.children)
        self.nodes = self.visible if not nodes else nodes

        # Initialize the surface and draw the map
        w, h = ENV.plotter.set_scale(self.nodes)
        self.base_map = pg.Surface((w,h), pg.SRCALPHA, 32)
        self.draw_map(self.base_map)
        self.map_surf = pg.Surface((w,h), pg.SRCALPHA, 32)
        self.map_surf.blit(self.base_map, (0,0))

        # Scale by height
        self.h = h
        self.scale = 1.

        # Compute start position. Center on the current node then find top-left corner
        sw, sh = size
        cx, cy = sw // 2, sh // 2
        nx, ny = ENV.plotter.get_pos(ENV.curr_node)
        self.x = max(min(PADDING, cx-nx), sw-w-PADDING)
        self.y = max(min(PADDING, cy-ny), sh-h-PADDING)

    def handle_event(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.finish_cb()
            if event.key == pg.K_UP:
                self.y += PAN_SPEED
            if event.key == pg.K_DOWN:
                self.y -= PAN_SPEED
            if event.key == pg.K_LEFT:
                self.x += PAN_SPEED
            if event.key == pg.K_RIGHT:
                self.x -= PAN_SPEED
        elif event.type == pg.MOUSEWHEEL:
            self.scale += event.y * SCALE_SPEED

    def update(self):
        # Scale map if needed
        self.scale = min(max(self.scale, MIN_SCALE), MAX_SCALE)
        h = self.scale * self.h
        if int(h) != self.map_surf.get_height():
            w = int(self.base_map.get_width() * self.scale)
            self.map_surf = pg.transform.smoothscale(self.base_map, (w,int(h)))
            

    def draw(self, surf: pg.Surface):
        # Center map on the parent surface then find the top-left corner
        w, h = surf.get_size()
        mw, mh = self.map_surf.get_size()
        cx, cy = w // 2, h // 2
        mcx, mcy = mw//2, mh//2
        mx, my = cx - mcx, cy - mcy

        # Offset and clip
        x, y = mx, my           # Center map if smaller than the screen
        if mw > w:
            x = max(min(PADDING, self.x), w-mw-PADDING)
        if mh > h:
            y = max(min(PADDING, self.y), h-mh-PADDING)

        self.x, self.y = x, y

        # Draw map
        # pg.draw.rect(surf, (255,0,0), pg.Rect(x, y, mw, mh))      # NOTE: Debugging rect
        surf.blit(self.map_surf, (x, y))

        # Draw hints
        hint = FONT_HINT.render("Move with arrow keys, zoom with scroll", True, COLOR_OUT)
        surf.blit(hint, (w - hint.get_width() - 10, 10))
        hint = FONT_HINT.render("Press (esc) to exit...", True, COLOR_OUT)
        surf.blit(hint, (w - hint.get_width() - 10, 15 + hint.get_height()))

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
        aapolygon(surf, (point1, point2, point3), COLOR_ARROW)
        filled_polygon(surf, (point1, point2, point3), COLOR_ARROW)

    def draw_node(self,surf, node):
        pos = ENV.plotter.get_pos(node)
        if not pos:
            return
        x, y = pos

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
