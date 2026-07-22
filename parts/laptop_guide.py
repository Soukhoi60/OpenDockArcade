"""
OpenDock Arcade
Removable laptop side guides
"""

from __future__ import annotations

import cadquery as cq

from config import cabinet


class LaptopGuide:
    """
    Guide latéral amovible.

    Deux versions :
    - left : côté gauche ;
    - right : côté droit.
    """

    def __init__(self, side: str) -> None:
        if side not in {"left", "right"}:
            raise ValueError(
                "Le côté doit être 'left' ou 'right'."
            )

        self.side = side

    def build(self) -> cq.Workplane:
        """Construit un guide latéral avec fixation M3."""

        base = (
            cq.Workplane("XY")
            .box(
                cabinet.guide_base_width,
                cabinet.guide_length,
                cabinet.guide_base_thickness,
                centered=(True, True, False),
            )
        )

        wall_x = (
            -cabinet.guide_base_width / 2.0
            + cabinet.guide_wall_thickness / 2.0
        )

        if self.side == "right":
            wall_x = -wall_x

        wall = (
            cq.Workplane("XY")
            .box(
                cabinet.guide_wall_thickness,
                cabinet.guide_length,
                cabinet.guide_height,
                centered=(True, True, False),
            )
            .translate(
                (
                    wall_x,
                    0,
                    cabinet.guide_base_thickness - 0.2,
                )
            )
        )

        guide = base.union(wall)

        # Trou traversant M3 au centre du guide.
        screw_hole = (
            cq.Workplane("XY")
            .circle(
                cabinet.guide_screw_diameter / 2.0
            )
            .extrude(
                cabinet.guide_base_thickness + 0.4
            )
            .translate((0, 0, -0.2))
        )

        guide = guide.cut(screw_hole)

        # Logement de tête de vis accessible depuis le dessus.
        head_pocket = (
            cq.Workplane("XY")
            .circle(
                cabinet.guide_screw_head_diameter / 2.0
            )
            .extrude(
                cabinet.guide_screw_head_depth + 0.2
            )
            .translate(
                (
                    0,
                    0,
                    cabinet.guide_base_thickness
                    - cabinet.guide_screw_head_depth
                    - 0.1,
                )
            )
        )

        guide = guide.cut(head_pocket)

        # L'arrondi est seulement esthétique.
        # Certaines versions de CadQuery échouent sur cette géométrie.
        try:
            guide = (
                guide
                .edges("|Z")
                .fillet(cabinet.guide_corner_radius)
            )
        except Exception:
            print(
                "Avertissement : arrondi impossible sur le guide. "
                "La pièce sera générée sans arrondi."
            )

        return guide.clean()