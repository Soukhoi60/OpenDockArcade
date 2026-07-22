"""
OpenDock Arcade
Removable laptop rear stop
"""

from __future__ import annotations

import cadquery as cq

from config import cabinet


class LaptopRearStop:
    """
    Butée arrière amovible.

    La paroi verticale est située du côté avant de la pièce,
    afin de venir au contact du bord arrière du portable.
    """

    def build(self) -> cq.Workplane:
        """Construit une butée arrière avec fixation M3."""

        base = (
            cq.Workplane("XY")
            .box(
                cabinet.rear_stop_base_width,
                cabinet.rear_stop_base_depth,
                cabinet.rear_stop_base_thickness,
                centered=(True, True, False),
            )
        )

        wall_y = (
            -cabinet.rear_stop_base_depth / 2.0
            + cabinet.rear_stop_wall_thickness / 2.0
        )

        wall = (
            cq.Workplane("XY")
            .box(
                cabinet.rear_stop_base_width,
                cabinet.rear_stop_wall_thickness,
                cabinet.rear_stop_wall_height,
                centered=(True, True, False),
            )
            .translate(
                (
                    0,
                    wall_y,
                    cabinet.rear_stop_base_thickness - 0.2,
                )
            )
        )

        stop = base.union(wall)

        # Trou traversant pour une vis M3.
        screw_hole = (
            cq.Workplane("XY")
            .circle(
                cabinet.rear_stop_screw_diameter / 2.0
            )
            .extrude(
                cabinet.rear_stop_base_thickness + 0.4
            )
            .translate((0, 0, -0.2))
        )

        stop = stop.cut(screw_hole)

        # Logement de tête de vis accessible depuis le dessus.
        head_pocket_z = (
            cabinet.rear_stop_base_thickness
            - cabinet.rear_stop_screw_head_depth
            - 0.1
        )

        head_pocket = (
            cq.Workplane("XY")
            .circle(
                cabinet.rear_stop_screw_head_diameter / 2.0
            )
            .extrude(
                cabinet.rear_stop_screw_head_depth + 0.2
            )
            .translate((0, 0, head_pocket_z))
        )

        stop = stop.cut(head_pocket)

        return stop.clean()