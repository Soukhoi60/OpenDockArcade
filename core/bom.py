"""
OpenDock Arcade
Bill of materials generator
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class BOMItem:
    """Élément de la nomenclature générale."""

    category: str
    name: str
    quantity: int
    material: str
    reference: str = ""
    notes: str = ""


def write_bom(
    items: Iterable[BOMItem],
    output_path: Path,
) -> None:
    """Écrit la nomenclature générale au format CSV."""

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
                "Catégorie",
                "Élément",
                "Quantité",
                "Matériau",
                "Référence",
                "Notes",
            ]
        )

        for item in items:
            writer.writerow(
                [
                    item.category,
                    item.name,
                    item.quantity,
                    item.material,
                    item.reference,
                    item.notes,
                ]
            )