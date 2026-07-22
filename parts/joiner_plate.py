"""
OpenDock Arcade
Modular chassis joining plates
"""

from __future__ import annotations

import cadquery as cq

from config import cabinet


class JoinerPlate:
    """
    Plaque d'assemblage placée sous le châssis.

    Deux orientations sont disponibles :
    - horizontal : liaison gauche/droite ;
    - vertical : liaison avant/arrière.
    """

    def __init__(self, orientation: str = "horizontal") -> None:
        if orientation not in {"horizontal", "vertical"}:
            raise ValueError(
                "L'orientation doit être 'horizontal' ou 'vertical'."
            )

        self.orientation = orientation

    def _dimensions(self) -> tuple[float, float]:
        """Retourne la largeur X et la profondeur Y."""

        if self.orientation == "horizontal":
            return (
                cabinet.joiner_plate_length,
                cabinet.joiner_plate_width,
            )

        return (
            cabinet.joiner_plate_width,
            cabinet.joiner_plate_length,
        )

    def _hole_positions(self) -> list[tuple[float, float]]:
        """Retourne les positions des deux vis."""

        half_spacing = cabinet.joiner_hole_spacing / 2.0

        if self.orientation == "horizontal":
            return [
                (-half_spacing, 0.0),
                (half_spacing, 0.0),
            ]

        return [
            (0.0, -half_spacing),
            (0.0, half_spacing),
        ]

    def build(self) -> cq.Workplane:
        """Construit la plaque avec trous et logements de têtes de vis."""

        width, depth = self._dimensions()

        plate = (
            cq.Workplane("XY")
            .box(
                width,
                depth,
                cabinet.joiner_plate_thickness,
                centered=(True, True, False),
            )
        )

        for x, y in self._hole_positions():
            # Trou traversant pour la vis M3.
            through_hole = (
                cq.Workplane("XY")
                .center(x, y)
                .circle(cabinet.joiner_screw_diameter / 2.0)
                .extrude(
                    cabinet.joiner_plate_thickness + 0.4
                )
                .translate((0, 0, -0.2))
            )

            plate = plate.cut(through_hole)

            # Logement de la tête de vis sous la plaque.
            head_pocket = (
                cq.Workplane("XY")
                .center(x, y)
                .circle(
                    cabinet.joiner_screw_head_diameter / 2.0
                )
                .extrude(
                    cabinet.joiner_screw_head_depth + 0.2
                )
                .translate((0, 0, -0.1))
            )

            plate = plate.cut(head_pocket)

        return plate.clean()