"""
OpenDock Arcade
M3 screw clearance calibration coupon
"""

from __future__ import annotations

import cadquery as cq


class M3ScrewTestCoupon:
    """
    Éprouvette de calibration pour vis M3.

    Elle permet de tester :

    - le diamètre du trou traversant ;
    - le passage réel de la vis après impression ;
    - le logement d'une tête de vis cylindrique.

    Le nombre de repères en relief identifie le diamètre :

    - 1 repère : 3,0 mm
    - 2 repères : 3,2 mm
    - 3 repères : 3,4 mm
    - 4 repères : 3,6 mm
    - 5 repères : 3,8 mm
    """

    HOLE_DIAMETERS = (
        3.0,
        3.2,
        3.4,
        3.6,
        3.8,
    )

    COUPON_LENGTH = 90.0
    COUPON_WIDTH = 28.0
    COUPON_THICKNESS = 7.0

    HOLE_SPACING = 16.0

    HEAD_DIAMETER = 6.5
    HEAD_DEPTH = 2.4

    MARKER_DIAMETER = 1.8
    MARKER_HEIGHT = 0.8
    MARKER_SPACING = 3.0

    CORNER_RADIUS = 3.0

    def _hole_positions(self) -> list[float]:
        """Retourne les positions X des cinq trous."""

        count = len(self.HOLE_DIAMETERS)

        total_width = (
            count - 1
        ) * self.HOLE_SPACING

        first_x = -total_width / 2.0

        return [
            first_x + index * self.HOLE_SPACING
            for index in range(count)
        ]

    def _build_base(self) -> cq.Workplane:
        """Construit la base de l’éprouvette."""

        base = (
            cq.Workplane("XY")
            .box(
                self.COUPON_LENGTH,
                self.COUPON_WIDTH,
                self.COUPON_THICKNESS,
                centered=(True, True, False),
            )
        )

        try:
            base = (
                base
                .edges("|Z")
                .fillet(self.CORNER_RADIUS)
            )
        except Exception:
            print(
                "Avertissement : arrondi impossible sur "
                "l’éprouvette de vis M3."
            )

        return base

    def _cut_clearance_holes(
        self,
        coupon: cq.Workplane,
    ) -> cq.Workplane:
        """Découpe les cinq trous traversants."""

        result = coupon

        for x, diameter in zip(
            self._hole_positions(),
            self.HOLE_DIAMETERS,
        ):
            hole = (
                cq.Workplane("XY")
                .circle(diameter / 2.0)
                .extrude(
                    self.COUPON_THICKNESS + 0.4
                )
                .translate(
                    (
                        x,
                        0,
                        -0.2,
                    )
                )
            )

            result = result.cut(hole)

        return result

    def _cut_head_pockets(
        self,
        coupon: cq.Workplane,
    ) -> cq.Workplane:
        """
        Découpe les logements supérieurs des têtes de vis.

        Tous les logements utilisent le même diamètre.
        Seul le trou traversant change.
        """

        result = coupon

        pocket_start_z = (
            self.COUPON_THICKNESS
            - self.HEAD_DEPTH
        )

        for x in self._hole_positions():
            pocket = (
                cq.Workplane("XY")
                .circle(self.HEAD_DIAMETER / 2.0)
                .extrude(self.HEAD_DEPTH + 0.2)
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
        """Ajoute les repères tactiles identifiant les trous."""

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
            group_width = (
                hole_index - 1
            ) * self.MARKER_SPACING

            first_marker_x = (
                hole_x
                - group_width / 2.0
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

        coupon = self._cut_clearance_holes(
            coupon
        )

        coupon = self._cut_head_pockets(
            coupon
        )

        coupon = self._add_markers(
            coupon
        )

        return coupon.clean()