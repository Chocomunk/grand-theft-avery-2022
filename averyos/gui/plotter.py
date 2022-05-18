from __future__ import annotations

import math
from typing import List, Tuple
from abc import ABC, abstractmethod

from system.filesystem import Node


PADDING = 5


class Plotter(ABC):

    def __init__(self, radius: int=50):
        self.r = radius

    def set_scale(self, nodes: List[Node]):
        """ 
        Tell the plotter to plot w.r.t. the given set of nodes
        Arguments:
            nodes: The list of nodes that will be considered in plotting
        Returns:
            (width, height): The dimensions of the plotting region
        """
        w, h = self._node_dims(nodes)

        width = (w + 2*self.r)
        height = (h + 2*self.r)
        return int(width) + PADDING, int(height) + PADDING

    def get_pos(self, node: Node) -> Tuple[int, int]:
        """ Returns (x, y): The center of the node to plot """
        p = self._node_pos(node)
        if p:
            return int(p[0]), int(p[1])

    @abstractmethod
    def _node_dims(self, nodes: List[Node]) -> Tuple[int, int]:
        """ Returns the unscaled (width, height) of the nodes """
        pass

    @abstractmethod
    def _node_pos(self, node: Node) -> Tuple[int, int]:
        """ Returns the unscaled center of the node to plot """
        pass


class MeshPlotter(Plotter):

    def __init__(self, pts: List, ids: List[int], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids = {v: i for i, v in enumerate(ids)}
        self.points = pts
        self.l, self.t = 0, 0

    def transform(self, scale=1, angle=0, shift=(0,0)):
        """ 
        Transforms all points in the order: scale -> rot -> shift.
        Angles are in degrees
        """
        c = math.cos(math.radians(-angle))
        s = math.sin(math.radians(-angle))
        def _tf(p):
            x,y = p[0]*scale, p[1]*scale
            return c*x - s*y + shift[0], s*x + c*y + shift[1]
        pts = [_tf(p) for p in self.points]
        return MeshPlotter(pts, self.ids, self.r)

    def extend(self, other: MeshPlotter) -> MeshPlotter:
        if len(set(self.ids).intersection(set(other.ids))):
            raise KeyError("Overlapping MeshPlotter node ids")
        l = len(self.points)
        new_ids = {v: i+l for v,i in other.ids.items()}     # Shift id refs
        self.ids.update(new_ids)
        self.points.extend(other.points)
        return self

    def id_to_point(self, i):
        return self.points[self.ids[i]]

    def _node_dims(self, nodes: List[Node]):
        ids = [n.id for n in nodes if n.id in self.ids]
        self.l, self.t, w, h = self.pts_dims([self.id_to_point(i) for i in ids])
        return w, h

    def _node_pos(self, node: Node):
        if node.id in self.ids:
            x, y = self.id_to_point(node.id)
            u = self.r + x - self.l
            v = self.r + y - self.t
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_id = 0

    def _node_dims(self, nodes: List[Node]):
        ids = [n.id for n in nodes]
        self.min_id = min(ids)
        max_id = max(ids)
        self.d = math.ceil(math.sqrt(max_id - self.min_id + 1))

        w = 4 * self.r * (self.d - 1)
        h = 4 * self.r * (max_id // self.d)
        return w, h

    def _node_pos(self, node: Node):
        rel_id = node.id - self.min_id          # Relative id

        # Get position on an nxn grid
        x, y = rel_id % self.d, rel_id // self.d
        return self.r + 4 * x * self.r, self.r + 4 * y * self.r
