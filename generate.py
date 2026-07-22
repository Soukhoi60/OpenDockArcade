"""
OpenDock Arcade Generator
"""

from __future__ import annotations

from core.export import export
from parts.chassis import Chassis
from parts.joiner_plate import JoinerPlate
from parts.tpu_pad import TPUPad


def main() -> None:
    print("Génération OpenDock Arcade...")
    print("")

    chassis_generator = Chassis()

    # Châssis complet pour visualisation.
    full_chassis = chassis_generator.build_full()

    export(
        "chassis_full",
        full_chassis,
    )

    # Quatre modules imprimables.
    modules = chassis_generator.build_modules()

    for module_name, module_model in modules.items():
        export(
            f"chassis_{module_name}",
            module_model,
        )

    # Plaques d'assemblage.
    horizontal_joiner = JoinerPlate(
        orientation="horizontal"
    ).build()

    vertical_joiner = JoinerPlate(
        orientation="vertical"
    ).build()

    export(
        "joiner_horizontal_x2",
        horizontal_joiner,
    )

    export(
        "joiner_vertical_x2",
        vertical_joiner,
    )

    # Patin TPU.
    pad = TPUPad().build()

    export(
        "tpu_pad_x6",
        pad,
    )

    print("")
    print("Génération terminée.")
    print("")
    print("Modules du châssis :")
    print("  - chassis_front_left")
    print("  - chassis_front_right")
    print("  - chassis_rear_left")
    print("  - chassis_rear_right")
    print("")
    print("Plaques d'assemblage :")
    print("  - joiner_horizontal_x2")
    print("  - joiner_vertical_x2")
    print("")
    print("Autres pièces :")
    print("  - tpu_pad_x6")
    print("")
    print("Quantités à imprimer :")
    print("  - chaque module du châssis : 1")
    print("  - plaque horizontale : 2")
    print("  - plaque verticale : 2")
    print("  - patin TPU : 6")
    print("")
    print("Visserie :")
    print("  - vis M3 : 8")
    print("  - inserts thermiques M3 : 8")


if __name__ == "__main__":
    main()