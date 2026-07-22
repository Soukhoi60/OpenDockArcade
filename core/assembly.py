"""
OpenDock Arcade
Assembly guide generator
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable


def write_assembly_guide(
    steps: Iterable[str],
    output_path: Path,
) -> None:
    """Écrit le guide d’assemblage au format Markdown."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    steps_list = list(steps)

    lines = [
        "# OpenDock Arcade — Guide d’assemblage",
        "",
        "Ce document est généré automatiquement par `generate.py`.",
        "",
        "## Avant de commencer",
        "",
        "- Vérifier que toutes les pièces imprimées sont propres.",
        "- Retirer les supports et ébavurer les trous.",
        "- Tester les inserts thermiques sur une pièce avant le montage final.",
        "- Ne pas installer le portable avant la fin de l’assemblage du châssis.",
        "",
        "## Ordre d’assemblage",
        "",
    ]

    for index, step in enumerate(
        steps_list,
        start=1,
    ):
        lines.append(
            f"### Étape {index}"
        )
        lines.append("")
        lines.append(step)
        lines.append("")

    lines.extend(
        [
            "## Vérifications finales",
            "",
            "- Le châssis repose à plat.",
            "- Les quatre modules sont correctement alignés.",
            "- Aucune tête de vis ne dépasse.",
            "- Les guides ne compriment pas le portable.",
            "- Les entrées et sorties d’air du portable restent dégagées.",
            "- Les câbles ne passent pas sous les patins.",
            "",
            "## Sécurité",
            "",
            "Ne jamais installer un insert thermique lorsque le portable "
            "ou un composant électronique se trouve dans le châssis.",
            "",
        ]
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )