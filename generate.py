"""
OpenDock Arcade Generator
"""

from __future__ import annotations

from core.export import export
from parts.chassis import Chassis
from parts.joiner_plate import JoinerPlate
from parts.laptop_guide import LaptopGuide
from parts.laptop_rear_stop import LaptopRearStop
from parts.tpu_pad import TPUPad


def main() -> None:
    print("Génération OpenDock Arcade...")
    print("")

    chassis_generator = Chassis()

    # Châssis complet.
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

    # Guides latéraux.
    left_guide = LaptopGuide(
        side="left"
    ).build()

    right_guide = LaptopGuide(
        side="right"
    ).build()

    export(
        "laptop_guide_left_x2",
        left_guide,
    )

    export(
        "laptop_guide_right_x2",
        right_guide,
    )

    # Butées arrière.
    rear_stop = LaptopRearStop().build()

    export(
        "laptop_rear_stop_x2",
        rear_stop,
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
    print("Quantités à imprimer :")
    print("  - chaque module du châssis : 1")
    print("  - plaque horizontale : 2")
    print("  - plaque verticale : 2")
    print("  - guide latéral gauche : 2")
    print("  - guide latéral droit : 2")
    print("  - patin TPU : 6")
    print("")
    print("Visserie totale actuelle :")
    print("  - vis M3 : 14")
    print("  - inserts thermiques M3 : 14")


if __name__ == "__main__":
    main()