"""
OpenDock CAD Engine
Primitive solids
"""

import cadquery as cq


class Solid:

    def __init__(self):
        self.model = None

    def box(self, x, y, z):

        self.model = (
            cq.Workplane("XY")
            .box(
                x,
                y,
                z,
                centered=(True, True, False)
            )
        )

        return self

    def cylinder(self, diameter, height):

        self.model = (
            cq.Workplane("XY")
            .circle(diameter / 2)
            .extrude(height)
        )

        return self

    def translate(self, x=0, y=0, z=0):

        self.model = self.model.translate((x, y, z))

        return self

    def union(self, other):

        self.model = self.model.union(other.model)

        return self

    def cut(self, other):

        self.model = self.model.cut(other.model)

        return self

    def fillet(self, radius):

        self.model = (
            self.model
            .edges("|Z")
            .fillet(radius)
        )

        return self

    def build(self):

        return self.model