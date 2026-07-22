"""
OpenDock Arcade
Hardware list generator
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class HardwareItem:
    """Élément de visserie ou composant non imprimé."""

    name: str
    quantity: int
    specification: str
    usage: str
    notes: str = ""


def write_hardware_list(
    items: Iterable[HardwareItem],
    output_path: Path,
) -> None:
    """Écrit la liste de visserie au format CSV."""

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
                "Élément",
                "Quantité",
                "Spécification",
                "Utilisation",
                "Notes",
            ]
        )

        for item in items:
            writer.writerow(
                [
                    item.name,
                    item.quantity,
                    item.specification,
                    item.usage,
                    item.notes,
                ]
            )