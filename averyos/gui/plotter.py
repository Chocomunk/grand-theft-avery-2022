import math
from typing import List, Tuple
from abc import ABC, abstractmethod

from system.filesystem import Node


PADDING = 5


class Plotter(ABC):

    def __init__(self, radius: int=50, size: Tuple[int, int]=(1920,1080), 
                    scale: float=1, max_radius: int=75):
        self._r = radius * scale
        self.max_r = max_radius
        self.scale = scale
        self.w, self.h = size

    def set_scale(self, nodes: List[Node], size: Tuple[int, int]=None):
        """ 
        Tell the plotter what the set of nodes are.
        Arguments:
            nodes: The list of nodes that will be considered in plotting
        Returns:
            (width, height): The dimensions of the plotting region
        """
        if size:
            self.w, self.h = size
        w, h = self._node_dims(nodes)

        if float(w)/h > float(self.w)/self.h:
            self.scale = (self.w - PADDING) / (w + 2*self._r)
        else:
            self.scale = (self.h - PADDING) / (h + 2*self._r)

        width = (w + 2*self._r) * self.scale
        height = (h + 2*self._r) * self.scale
        return int(width) + PADDING, int(height) + PADDING

    def get_pos(self, node: Node) -> Tuple[int, int]:
        """ Returns (x, y): The center of the node to plot """
        p = self._node_pos(node)
        if p:
            return int(p[0] * self.scale), int(p[1] * self.scale)

    @property
    def r(self):
        return min(int(self._r * self.scale), self.max_r)

    @abstractmethod
    def _node_dims(self, nodes: List[Node]) -> Tuple[int, int]:
        """ Returns the unscaled (width, height) of the nodes """
        pass

    @abstractmethod
    def _node_pos(self, node: Node) -> Tuple[int, int]:
        """ Returns the unscaled center of the node to plot """
        pass


class MeshPlotter(Plotter):

    def __init__(self, pts, radius: int=3, size: Tuple[int, int]=(1920,1080)):
        super().__init__(radius, size)
        self.points = pts
        self.l, self.t = 0, 0

    def _node_dims(self, nodes: List[Node]):
        ids = [n.id for n in nodes if n.id < len(self.points)]
        self.l, self.t, w, h = self.pts_dims([self.points[i] for i in ids])
        return w, h

    def _node_pos(self, node: Node):
        if node.id < len(self.points):
            x, y = self.points[node.id]
            u = self._r + x - self.l
            v = self._r + y - self.t
            return u, v
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

    def __init__(self, radius: int=50, size: Tuple[int, int]=(1920,1080), scale: float=1):
        super().__init__(radius, size, scale)
        self.min_id = 0

    def _node_dims(self, nodes: List[Node]):
        ids = [n.id for n in nodes]
        self.min_id = min(ids)
        max_id = max(ids)
        self.d = math.ceil(math.sqrt(max_id - self.min_id + 1))

        w = 4 * self._r * (self.d - 1)
        h = 4 * self._r * (max_id // self.d)
        return w, h

    def _node_pos(self, node: Node):
        rel_id = node.id - self.min_id          # Relative id

        # Get position on an nxn grid
        x, y = rel_id % self.d, rel_id // self.d
        return self._r + 4 * x * self._r, self._r + 4 * y * self._r
