"""
OpenDock Arcade
Frame Engine

Petite couche d'abstraction au-dessus de CadQuery pour construire
et modifier les éléments structurels de la borne.
"""

from __future__ import annotations

import cadquery as cq


class Frame:
    """Constructeur paramétrique de châssis."""

    def __init__(self) -> None:
        self.model: cq.Workplane | None = None

    def _require_model(self) -> cq.Workplane:
        if self.model is None:
            raise RuntimeError(
                "Le châssis n'existe pas encore. "
                "Appelez create_base() avant cette opération."
            )
        return self.model

    def create_base(
        self,
        width: float,
        depth: float,
        thickness: float,
    ) -> "Frame":
        """Crée la plaque extérieure initiale."""

        self.model = (
            cq.Workplane("XY")
            .box(
                width,
                depth,
                thickness,
                centered=(True, True, False),
            )
        )

        return self

    def hollow(self, border: float) -> "Frame":
        """Évide la plaque afin de créer un cadre périphérique."""

        model = self._require_model()
        bounds = model.val().BoundingBox()

        inner_width = bounds.xlen - 2.0 * border
        inner_depth = bounds.ylen - 2.0 * border

        if inner_width <= 0 or inner_depth <= 0:
            raise ValueError(
                "La bordure est trop grande pour les dimensions du châssis."
            )

        cutter = (
            cq.Workplane("XY")
            .box(
                inner_width,
                inner_depth,
                bounds.zlen + 2.0,
                centered=(True, True, False),
            )
            .translate((0, 0, -1.0))
        )

        self.model = model.cut(cutter)
        return self

    def add_box(
        self,
        *,
        x: float,
        y: float,
        z: float,
        width: float,
        depth: float,
        height: float,
    ) -> "Frame":
        """Ajoute un bloc rectangulaire au modèle."""

        model = self._require_model()

        solid = (
            cq.Workplane("XY")
            .box(
                width,
                depth,
                height,
                centered=(True, True, False),
            )
            .translate((x, y, z))
        )

        self.model = model.union(solid)
        return self

    def add_cylinder(
        self,
        *,
        x: float,
        y: float,
        z: float,
        diameter: float,
        height: float,
    ) -> "Frame":
        """Ajoute un cylindre au modèle."""

        model = self._require_model()

        solid = (
            cq.Workplane("XY")
            .circle(diameter / 2.0)
            .extrude(height)
            .translate((x, y, z))
        )

        self.model = model.union(solid)
        return self

    def cut_cylinder(
        self,
        *,
        x: float,
        y: float,
        z: float,
        diameter: float,
        depth: float,
    ) -> "Frame":
        """Découpe un logement ou un perçage cylindrique."""

        model = self._require_model()

        cutter = (
            cq.Workplane("XY")
            .circle(diameter / 2.0)
            .extrude(depth)
            .translate((x, y, z))
        )

        self.model = model.cut(cutter)
        return self

    def add_solid(self, solid: cq.Workplane) -> "Frame":
        """Fusionne un solide CadQuery existant."""

        model = self._require_model()
        self.model = model.union(solid)

        return self

    def cut_solid(self, solid: cq.Workplane) -> "Frame":
        """Soustrait un solide CadQuery existant."""

        model = self._require_model()
        self.model = model.cut(solid)

        return self

    def clean(self) -> "Frame":
        """Nettoie les arêtes résiduelles des opérations booléennes."""

        self.model = self._require_model().clean()
        return self

    def build(self) -> cq.Workplane:
        """Retourne le modèle CadQuery final."""

        return self._require_model()