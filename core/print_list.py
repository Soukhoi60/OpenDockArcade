"""
OpenDock Arcade
3D printing list generator
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class PrintItem:
    """Pièce devant être imprimée en 3D."""

    file_name: str
    part_name: str
    quantity: int
    material: str
    layer_height: str
    walls: int
    infill: str
    supports: str
    notes: str = ""


def write_print_list(
    items: Iterable[PrintItem],
    output_path: Path,
) -> None:
    """Écrit la liste d’impression au format CSV."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output_path.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as csv_file:
        writer = csv.writer(
            csv_file,
            delimiter=";",
        )

        writer.writerow(
            [
                "Fichier STL",
                "Pièce",
                "Quantité",
                "Matériau",
                "Hauteur de couche",
                "Parois",
                "Remplissage",
                "Supports",
                "Notes",
            ]
        )

        for item in items:
            writer.writerow(
                [
                    item.file_name,
                    item.part_name,
                    item.quantity,
                    item.material,
                    item.layer_height,
                    item.walls,
                    item.infill,
                    item.supports,
                    item.notes,
                ]
            )