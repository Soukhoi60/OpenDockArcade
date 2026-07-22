"""
OpenDock Arcade
Removable rear cable clip
"""

from __future__ import annotations

import cadquery as cq

from config import cabinet


class CableClip:
    """
    Clip arrière amovible pour guider les câbles.

    Le clip comporte :
    - une base vissée au châssis ;
    - un anneau vertical ;
    - une ouverture supérieure pour insérer le câble.
    """

    def build(self) -> cq.Workplane:
        """Construit le clip de câble complet."""

        base = (
            cq.Workplane("XY")
            .box(
                cabinet.cable_clip_base_width,
                cabinet.cable_clip_base_depth,
                cabinet.cable_clip_base_thickness,
                centered=(True, True, False),
            )
        )

        ring_center_z = (
            cabinet.cable_clip_base_thickness
            + cabinet.cable_clip_outer_diameter / 2.0
            - 0.5
        )

        # Anneau construit sur le plan XZ.
        outer_ring = (
            cq.Workplane("XZ")
            .circle(
                cabinet.cable_clip_outer_diameter / 2.0
            )
            .extrude(
                cabinet.cable_clip_ring_width,
                both=True,
            )
            .translate(
                (
                    0,
                    0,
                    ring_center_z,
                )
            )
        )

        inner_hole = (
            cq.Workplane("XZ")
            .circle(
                cabinet.cable_clip_inner_diameter / 2.0
            )
            .extrude(
                cabinet.cable_clip_ring_width + 2.0,
                both=True,
            )
            .translate(
                (
                    0,
                    0,
                    ring_center_z,
                )
            )
        )

        ring = outer_ring.cut(inner_hole)

        # Ouverture supérieure permettant de clipser le câble.
        opening = (
            cq.Workplane("XY")
            .box(
                cabinet.cable_clip_opening,
                cabinet.cable_clip_ring_width + 4.0,
                cabinet.cable_clip_outer_diameter,
                centered=(True, True, False),
            )
            .translate(
                (
                    0,
                    0,
                    ring_center_z,
                )
            )
        )

        ring = ring.cut(opening)

        clip = base.union(ring)

        # Trou traversant M3.
        screw_hole = (
            cq.Workplane("XY")
            .circle(
                cabinet.cable_clip_screw_diameter / 2.0
            )
            .extrude(
                cabinet.cable_clip_base_thickness + 0.4
            )
            .translate((0, 0, -0.2))
        )

        clip = clip.cut(screw_hole)

        # Logement de la tête de vis accessible depuis le dessus.
        head_pocket_z = (
            cabinet.cable_clip_base_thickness
            - cabinet.cable_clip_screw_head_depth
            - 0.1
        )

        head_pocket = (
            cq.Workplane("XY")
            .circle(
                cabinet.cable_clip_screw_head_diameter / 2.0
            )
            .extrude(
                cabinet.cable_clip_screw_head_depth + 0.2
            )
            .translate(
                (
                    0,
                    0,
                    head_pocket_z,
                )
            )
        )

        clip = clip.cut(head_pocket)

        return clip.clean()