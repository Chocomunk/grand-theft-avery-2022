import math
from typing import List, Tuple
from abc import ABC, abstractmethod

from system.filesystem import Node


PADDING = 5


class Plotter(ABC):

    def __init__(self, radius=50, scale=1080):
        self.base_r = radius
        self.r = radius
        self.base_scale = scale
        self.scale = scale

    def set_scale(self, scale):
        self.r = int(self.base_r * scale / self.base_scale)
        self.scale = scale

    @abstractmethod
    def set_nodes(self, nodes: List[Node]) -> Tuple[int, int]:
        """ 
        Tell the plotter what the set of nodes are.
        Arguments:
            nodes: The list of nodes that will be considered in plotting
        Returns:
            (width, height): The dimensions of the plotting region
        """
        pass

    @abstractmethod
    def get_pos(self, node: Node) -> Tuple[int, int]:
        """ Returns (x, y): The center of the node to plot """
        pass


class MeshPlotter(Plotter):

    def __init__(self, pts, radius=50, scale=1080):
        super().__init__(radius, scale)
        l, t, w, h = self.pts_dims(pts)
        norm = 1. / max(w,h)                    # Normalize largest dim to 1
        pts = [((x-l)*norm, (y-t)*norm) for (x,y) in pts]
        self.l, self.t = 0, 0
        self.points = pts

    def set_nodes(self, nodes: List[Node]):
        ids = [n.id for n in nodes if n.id < len(self.points)]
        self.l, self.t, w, h = self.pts_dims([self.points[i] for i in ids])
        width = w*self.scale + 2*self.r
        height = h*self.scale + 2*self.r
        return int(width) + PADDING, int(height) + PADDING

    def get_pos(self, node: Node):
        if node.id < len(self.points):
            x, y = self.points[node.id]
            u = self.r + (x - self.l) * self.scale
            v = self.r + (y - self.t) * self.scale
            return int(u), int(v)
        return None

    def pts_dims(self, pts):
        """ Returns (left, top, width, height) """
        xs = [x for x, _ in pts]
        ys = [y for _, y in pts]

        l = min(xs)
        r = max(xs)
        t = min(ys)
        b = max(ys)

        return l, t, r-l, b-t


class GridPlotter(Plotter):

    def __init__(self, radius=50):
        super().__init__(radius)
        self.r = radius
        self.min_id = 0

    def set_nodes(self, nodes: List[Node]):
        ids = [n.id for n in nodes]
        self.min_id = min(ids)
        max_id = max(ids)
        self.d = math.ceil(math.sqrt(max_id - self.min_id + 1))

        w = 4 * self.r * self.d - 2 * self.r
        h = 4 * self.r * (1 + max_id // self.d) - 2 * self.r
        return w + PADDING, h + PADDING

    def get_pos(self, node: Node):
        rel_id = node.id - self.min_id          # Relative id

        # Get position on an nxn grid
        x, y = rel_id % self.d, rel_id // self.d
        return self.r + 4 * x * self.r, self.r + 4 * y * self.r
