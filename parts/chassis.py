import cadquery as cq
from config import cabinet


class Chassis:

    def __init__(self):
        self.model = None

    def build(self):

        # Base
        outer = (
            cq.Workplane("XY")
            .box(
                cabinet.base_width,
                cabinet.base_depth,
                cabinet.base_thickness,
                centered=(True, True, False)
            )
        )

        # Découpe centrale
        inner = (
            cq.Workplane("XY")
            .box(
                cabinet.base_width - cabinet.rail_width * 2,
                cabinet.base_depth - cabinet.rail_width * 2,
                cabinet.base_thickness + 2,
                centered=(True, True, False)
            )
        )

        frame = outer.cut(inner)

        # Traverse avant
        front = (
            cq.Workplane("XY")
            .box(
                cabinet.base_width - cabinet.rail_width * 2,
                cabinet.crossbar_width,
                cabinet.rail_height,
                centered=(True, True, False)
            )
            .translate((0,
                        -(cabinet.base_depth/2) + cabinet.rail_width + cabinet.crossbar_width/2,
                        cabinet.base_thickness))
        )

        # Traverse centrale
        center = (
            cq.Workplane("XY")
            .box(
                cabinet.base_width - cabinet.rail_width * 2,
                cabinet.crossbar_width,
                cabinet.rail_height,
                centered=(True, True, False)
            )
            .translate((0,0,cabinet.base_thickness))
        )

        # Traverse arrière
        rear = (
            cq.Workplane("XY")
            .box(
                cabinet.base_width - cabinet.rail_width * 2,
                cabinet.crossbar_width,
                cabinet.rail_height,
                centered=(True, True, False)
            )
            .translate((0,
                        cabinet.base_depth/2 - cabinet.rail_width - cabinet.crossbar_width/2,
                        cabinet.base_thickness))
        )

        self.model = frame.union(front).union(center).union(rear)

        return self.model