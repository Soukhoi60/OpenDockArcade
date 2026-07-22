"""
OpenDock Arcade
Universal side panel section joiner
"""

from __future__ import annotations

import cadquery as cq

from config import cabinet


class SidePanelJoiner:
    """
    Plaque universelle d’assemblage des sections de flanc.

    La plaque comporte deux logements pour inserts thermiques M3.

    Elle peut être tournée pendant l’assemblage :

    - horizontalement pour une séparation verticale ;
    - verticalement pour une séparation horizontale.
    """

    def _build_base(self) -> cq.Workplane:
        """Construit la plaque rectangulaire."""

        joiner = (
            cq.Workplane("XY")
            .box(
                cabinet.side_panel_joiner_length,
                cabinet.side_panel_joiner_width,
                cabinet.side_panel_joiner_thickness,
                centered=(True, True, False),
            )
        )

        radius = (
            cabinet.side_panel_joiner_corner_radius
        )

        if radius > 0:
            try:
                joiner = (
                    joiner
                    .edges("|Z")
                    .fillet(radius)
                )
            except Exception:
                print(
                    "Avertissement : impossible d’appliquer "
                    "les arrondis de la plaque de flanc."
                )

        return joiner

    def _insert_positions(
        self,
    ) -> list[tuple[float, float]]:
        """Retourne les positions des deux inserts."""

        offset = (
            cabinet.side_panel_joiner_hole_offset
        )

        return [
            (-offset, 0.0),
            (offset, 0.0),
        ]

    def _cut_insert_pockets(
        self,
        joiner: cq.Workplane,
    ) -> cq.Workplane:
        """
        Découpe les logements d’inserts depuis la face supérieure.

        Cette face doit être placée contre le flanc.
        """

        result = joiner

        pocket_start_z = (
            cabinet.side_panel_joiner_thickness
            - cabinet.side_panel_joiner_insert_depth
            - 0.1
        )

        for x, y in self._insert_positions():
            pocket = (
                cq.Workplane("XY")
                .circle(
                    cabinet.side_panel_joiner_insert_diameter
                    / 2.0
                )
                .extrude(
                    cabinet.side_panel_joiner_insert_depth
                    + 0.2
                )
                .translate(
                    (
                        x,
                        y,
                        pocket_start_z,
                    )
                )
            )

            result = result.cut(pocket)

        return result

    def build(self) -> cq.Workplane:
        """Construit la plaque complète."""

        joiner = self._build_base()

        joiner = self._cut_insert_pockets(
            joiner
        )

        return joiner.clean()