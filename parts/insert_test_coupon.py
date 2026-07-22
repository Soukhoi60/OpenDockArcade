"""
OpenDock Arcade
M3 heat-set insert calibration coupon
"""

from __future__ import annotations

import cadquery as cq


class InsertTestCoupon:
    """
    Éprouvette de calibration pour inserts thermiques M3.

    La pièce comporte cinq logements de diamètres différents.
    Un nombre de petits repères en relief identifie chaque logement :

    - 1 repère : 4,2 mm
    - 2 repères : 4,4 mm
    - 3 repères : 4,6 mm
    - 4 repères : 4,8 mm
    - 5 repères : 5,0 mm
    """

    DIAMETERS = (
        4.2,
        4.4,
        4.6,
        4.8,
        5.0,
    )

    COUPON_LENGTH = 90.0
    COUPON_WIDTH = 24.0
    COUPON_THICKNESS = 8.0

    HOLE_SPACING = 16.0
    HOLE_DEPTH = 6.2

    MARKER_DIAMETER = 1.8
    MARKER_HEIGHT = 0.8
    MARKER_SPACING = 3.0

    CORNER_RADIUS = 3.0

    def _hole_positions(self) -> list[float]:
        """Retourne les positions X des cinq logements."""

        count = len(self.DIAMETERS)
        total_width = (count - 1) * self.HOLE_SPACING

        first_x = -total_width / 2.0

        return [
            first_x + index * self.HOLE_SPACING
            for index in range(count)
        ]

    def _build_base(self) -> cq.Workplane:
        """Construit la base rectangulaire de l’éprouvette."""

        base = (
            cq.Workplane("XY")
            .box(
                self.COUPON_LENGTH,
                self.COUPON_WIDTH,
                self.COUPON_THICKNESS,
                centered=(True, True, False),
            )
        )

        # L’arrondi est esthétique et ne doit jamais bloquer
        # la génération de la pièce.
        try:
            base = (
                base
                .edges("|Z")
                .fillet(self.CORNER_RADIUS)
            )
        except Exception:
            print(
                "Avertissement : arrondi impossible sur "
                "l’éprouvette d’inserts."
            )

        return base

    def _cut_insert_pockets(
        self,
        coupon: cq.Workplane,
    ) -> cq.Workplane:
        """Découpe les cinq logements d’inserts."""

        result = coupon

        pocket_start_z = (
            self.COUPON_THICKNESS
            - self.HOLE_DEPTH
        )

        for x, diameter in zip(
            self._hole_positions(),
            self.DIAMETERS,
        ):
            pocket = (
                cq.Workplane("XY")
                .circle(diameter / 2.0)
                .extrude(self.HOLE_DEPTH + 0.2)
                .translate(
                    (
                        x,
                        0,
                        pocket_start_z - 0.1,
                    )
                )
            )

            result = result.cut(pocket)

        return result

    def _add_markers(
        self,
        coupon: cq.Workplane,
    ) -> cq.Workplane:
        """
        Ajoute des repères tactiles en relief.

        Le nombre de repères indique le diamètre testé.
        """

        result = coupon

        marker_y = (
            -self.COUPON_WIDTH / 2.0
            + 3.0
        )

        marker_z = self.COUPON_THICKNESS

        for hole_index, hole_x in enumerate(
            self._hole_positions(),
            start=1,
        ):
            marker_group_width = (
                (hole_index - 1)
                * self.MARKER_SPACING
            )

            first_marker_x = (
                hole_x
                - marker_group_width / 2.0
            )

            for marker_index in range(hole_index):
                marker_x = (
                    first_marker_x
                    + marker_index
                    * self.MARKER_SPACING
                )

                marker = (
                    cq.Workplane("XY")
                    .circle(
                        self.MARKER_DIAMETER / 2.0
                    )
                    .extrude(self.MARKER_HEIGHT)
                    .translate(
                        (
                            marker_x,
                            marker_y,
                            marker_z,
                        )
                    )
                )

                result = result.union(marker)

        return result

    def build(self) -> cq.Workplane:
        """Construit l’éprouvette complète."""

        coupon = self._build_base()

        coupon = self._cut_insert_pockets(
            coupon
        )

        coupon = self._add_markers(
            coupon
        )

        return coupon.clean()