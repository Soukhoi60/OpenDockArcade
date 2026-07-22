"""
OpenDock Arcade
Reusable mechanical features
"""

from __future__ import annotations

import cadquery as cq


def tpu_pad(
    diameter: float,
    height: float,
) -> cq.Workplane:
    """Crée un patin TPU cylindrique imprimable séparément."""

    if diameter <= 0 or height <= 0:
        raise ValueError(
            "Le diamètre et la hauteur du patin doivent être positifs."
        )

    return (
        cq.Workplane("XY")
        .circle(diameter / 2.0)
        .extrude(height)
        .edges(">Z")
        .chamfer(min(0.6, height / 3.0))
    )


def cylindrical_pocket(
    diameter: float,
    depth: float,
    *,
    extra_depth: float = 0.2,
) -> cq.Workplane:
    """
    Crée le volume de découpe d'un logement cylindrique.

    L'excédent évite les surfaces coplanaires pendant les opérations
    booléennes.
    """

    if diameter <= 0 or depth <= 0:
        raise ValueError(
            "Le diamètre et la profondeur doivent être positifs."
        )

    return (
        cq.Workplane("XY")
        .circle(diameter / 2.0)
        .extrude(depth + extra_depth)
    )


def heat_insert_m3_pocket(
    diameter: float = 4.6,
    depth: float = 5.2,
    lead_in_diameter: float = 5.6,
    lead_in_depth: float = 0.8,
) -> cq.Workplane:
    """
    Crée un logement simple pour insert thermique M3.

    La première portion légèrement plus large facilite le centrage
    de l'insert avant sa pose au fer à souder.
    """

    if lead_in_depth >= depth:
        raise ValueError(
            "La profondeur d'entrée doit être inférieure "
            "à la profondeur totale."
        )

    main_hole = (
        cq.Workplane("XY")
        .circle(diameter / 2.0)
        .extrude(depth)
    )

    lead_in = (
        cq.Workplane("XY")
        .circle(lead_in_diameter / 2.0)
        .extrude(lead_in_depth)
    )

    return main_hole.union(lead_in)