import cadquery as cq

from config import cabinet
from config import laptop


class LaptopHolder:

    def __init__(self):
        self.model = cq.Workplane("XY")

    def build(self):

        x = laptop.width / 2 - 30

        y1 = cabinet.laptop_offset_front + 30
        y2 = cabinet.laptop_offset_front + laptop.depth / 2
        y3 = cabinet.laptop_offset_front + laptop.depth - 30

        pads = []

        for xx in (-x, x):

            for yy in (y1, y2, y3):

                pad = (
                    cq.Workplane("XY")
                    .cylinder(
                        cabinet.pad_height,
                        cabinet.pad_diameter / 2
                    )
                    .translate((xx,
                                yy - cabinet.base_depth / 2,
                                cabinet.base_thickness))
                )

                pads.append(pad)

        model = pads[0]

        for p in pads[1:]:
            model = model.union(p)

        guide_x = laptop.width / 2 + cabinet.guide_clearance

        left = (
            cq.Workplane("XY")
            .box(
                cabinet.guide_width,
                laptop.depth,
                cabinet.guide_height,
                centered=(True, False, False)
            )
            .translate((
                -guide_x,
                cabinet.laptop_offset_front - cabinet.base_depth / 2,
                cabinet.base_thickness
            ))
        )

        right = (
            cq.Workplane("XY")
            .box(
                cabinet.guide_width,
                laptop.depth,
                cabinet.guide_height,
                centered=(True, False, False)
            )
            .translate((
                guide_x,
                cabinet.laptop_offset_front - cabinet.base_depth / 2,
                cabinet.base_thickness
            ))
        )

        stop = (
            cq.Workplane("XY")
            .box(
                laptop.width,
                cabinet.rear_stop_thickness,
                cabinet.rear_stop_height,
                centered=(True, False, False)
            )
            .translate((
                0,
                cabinet.laptop_offset_front + laptop.depth - cabinet.base_depth / 2,
                cabinet.base_thickness
            ))
        )

        return model.union(left).union(right).union(stop)