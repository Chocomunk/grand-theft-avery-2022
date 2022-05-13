from typing import List

from system.filesystem import Node


class Mesh:

    def __init__(self, pts, scale=1.0):
        pts = [(x*scale, y*scale) for (x,y) in pts]
        l, t, self.w, self.h = self.pts_dims(pts)
        pts = [(x-l, y-t) for (x,y) in pts]

        self.points = pts

    def node_dims(self, nodes: List[Node]):
        """ Returns (left, top, width, height) """
        return self.pts_dims([self.points[n.id] for n in nodes])

    def pts_dims(self, pts):
        """ Returns (left, top, width, height) """
        xs = [x for x, _ in pts]
        ys = [y for _, y in pts]

        l = min(xs)
        r = max(xs)
        t = min(ys)
        b = max(ys)

        return l, t, (r-l), (b-t)