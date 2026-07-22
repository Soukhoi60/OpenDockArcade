"""
OpenDock Arcade
Fasteners Library
"""

from dataclasses import dataclass

import cadquery as cq


@dataclass
class HeatInsertM3:

    diameter: float = 4.6
    depth: float = 5.2
    lead_in: float = 0.6

    def cut(self):

        hole = (
            cq.Workplane("XY")
            .circle(self.diameter/2)
            .extrude(self.depth)
        )

        chamfer = (
            cq.Workplane("XY")
            .cone(
                self.lead_in,
                self.diameter/2 + 0.5,
                self.diameter/2
            )
            .translate((0,0,self.depth))
        )

        return hole.union(chamfer)