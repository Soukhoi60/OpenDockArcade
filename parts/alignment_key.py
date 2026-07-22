"""
OpenDock Arcade
Side panel alignment key
"""

from __future__ import annotations

import cadquery as cq

from config import cabinet


class AlignmentKey:
    """
    Clé universelle d’alignement des sections de flanc.

    La clé est insérée dans un logement peu profond situé
    sur la face intérieure du flanc.
    """

    def _validate_parameters(self) -> None:
        """Vérifie les dimensions de la clé."""

        if cabinet.side_panel_alignment_key_length <= 0:
            raise ValueError(
                "side_panel_alignment_key_length doit être positif."
            )

        if cabinet.side_panel_alignment_key_width <= 0:
            raise ValueError(
                "side_panel_alignment_key_width doit être positif."
            )

        if cabinet.side_panel_alignment_key_thickness <= 0:
            raise ValueError(
                "side_panel_alignment_key_thickness doit être positif."
            )

        if (
            cabinet.side_panel_alignment_key_thickness
            >= cabinet.side_panel_thickness
        ):
            raise ValueError(
                "La clé d’alignement doit être moins épaisse "
                "que le flanc."
            )

    def _build_base(self) -> cq.Workplane:
        """Construit la forme principale de la clé."""

        return (
            cq.Workplane("XY")
            .box(
                cabinet.side_panel_alignment_key_length,
                cabinet.side_panel_alignment_key_width,
                cabinet.side_panel_alignment_key_thickness,
                centered=(True, True, False),
            )
        )

    def _apply_corner_radius(
        self,
        key: cq.Workplane,
    ) -> cq.Workplane:
        """Arrondit les coins verticaux."""

        radius = (
            cabinet.side_panel_alignment_key_corner_radius
        )

        if radius <= 0:
            return key

        try:
            return (
                key
                .edges("|Z")
                .fillet(radius)
            )
        except Exception:
            print(
                "Avertissement : impossible d’arrondir "
                "les coins de la clé d’alignement."
            )

            return key

    def _apply_entry_chamfer(
        self,
        key: cq.Workplane,
    ) -> cq.Workplane:
        """Ajoute un léger chanfrein sur la face supérieure."""

        chamfer = (
            cabinet.side_panel_alignment_key_chamfer
        )

        if chamfer <= 0:
            return key

        try:
            return (
                key
                .edges(">Z")
                .chamfer(chamfer)
            )
        except Exception:
            print(
                "Avertissement : impossible d’ajouter "
                "le chanfrein de la clé d’alignement."
            )

            return key

    def build(self) -> cq.Workplane:
        """Construit la clé complète."""

        self._validate_parameters()

        key = self._build_base()

        key = self._apply_corner_radius(
            key
        )

        key = self._apply_entry_chamfer(
            key
        )

        bounding_box = (
            key
            .val()
            .BoundingBox()
        )

        key = key.translate(
            (
                -(
                    bounding_box.xmin
                    + bounding_box.xmax
                ) / 2.0,
                -(
                    bounding_box.ymin
                    + bounding_box.ymax
                ) / 2.0,
                -bounding_box.zmin,
            )
        )

        return key.clean()