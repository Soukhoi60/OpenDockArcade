"""
OpenDock Arcade Generator
"""

from __future__ import annotations

from pathlib import Path

from core.assembly import write_assembly_guide
from core.bom import BOMItem, write_bom
from core.export import export
from core.hardware import HardwareItem, write_hardware_list
from core.print_list import PrintItem, write_print_list

from parts.cable_clip import CableClip
from parts.chassis import Chassis
from parts.insert_test_coupon import InsertTestCoupon
from parts.joiner_plate import JoinerPlate
from parts.laptop_guide import LaptopGuide
from parts.laptop_rear_stop import LaptopRearStop
from parts.m3_screw_test_coupon import M3ScrewTestCoupon
from parts.screen_support import ScreenSupport
from parts.side_panel import SidePanel
from parts.side_panel_joiner import SidePanelJoiner
from parts.tpu_pad import TPUPad


OUTPUT_DIRECTORY = Path("output")
DOCS_DIRECTORY = OUTPUT_DIRECTORY / "docs"


def generate_cad_files() -> None:
    """Génère tous les fichiers STEP et STL."""

    print("Génération des modèles 3D...")
    print("")

    chassis_generator = Chassis()

    # Châssis complet de référence.
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

    # Plaques d’assemblage.
    horizontal_joiner = JoinerPlate(
        orientation="horizontal",
    ).build()

    vertical_joiner = JoinerPlate(
        orientation="vertical",
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
        side="left",
    ).build()

    right_guide = LaptopGuide(
        side="right",
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

    # Clips de câbles arrière.
    cable_clip = CableClip().build()

    export(
        "cable_clip_x2",
        cable_clip,
    )

    # Supports arrière de l’écran.
    screen_support = ScreenSupport().build()

    export(
        "screen_support_x2",
        screen_support,
    )

    # ============================================================
    # Flanc gauche complet et sections imprimables
    # ============================================================

    left_side_panel_generator = SidePanel(
        side="left",
    )

    left_side_panel = (
        left_side_panel_generator.build()
    )

    export(
        "side_panel_left",
        left_side_panel,
    )

    left_side_sections = (
        left_side_panel_generator
        .build_printable_sections()
    )

    for section_name, section_model in (
        left_side_sections.items()
    ):
        export(
            f"side_panel_left_{section_name}",
            section_model,
        )

    # ============================================================
    # Flanc droit complet et sections imprimables
    # ============================================================

    right_side_panel_generator = SidePanel(
        side="right",
    )

    right_side_panel = (
        right_side_panel_generator.build()
    )

    export(
        "side_panel_right",
        right_side_panel,
    )

    right_side_sections = (
        right_side_panel_generator
        .build_printable_sections()
    )

    for section_name, section_model in (
        right_side_sections.items()
    ):
        export(
            f"side_panel_right_{section_name}",
            section_model,
        )

    # Plaque universelle d’assemblage des sections de flanc.
    side_panel_joiner = SidePanelJoiner().build()

    export(
        "side_panel_joiner_x14",
        side_panel_joiner,
    )
    # Patin souple.
    pad = TPUPad().build()

    export(
        "tpu_pad_x6",
        pad,
    )

    # Éprouvette de calibration pour inserts thermiques M3.
    insert_test_coupon = InsertTestCoupon().build()

    export(
        "insert_test_coupon",
        insert_test_coupon,
    )

    # Éprouvette de calibration pour les vis M3.
    screw_test_coupon = M3ScrewTestCoupon().build()

    export(
        "m3_screw_test_coupon",
        screw_test_coupon,
    )


def generate_bom() -> None:
    """Génère la nomenclature générale du projet."""

    items = [
        BOMItem(
            category="Structure de borne",
            name="Plaque de jonction de flanc",
            quantity=14,
            material="PETG",
            reference="side_panel_joiner_x14.stl",
            notes=(
                "Sept plaques sur la face intérieure "
                "de chaque flanc."
            ),
        ),
        BOMItem(
            category="Visserie",
            name="Vis M3 pour les flancs",
            quantity=28,
            material="Acier",
            reference="M3",
            notes=(
                "Deux vis par plaque de jonction."
            ),
        ),
        BOMItem(
            category="Visserie",
            name="Insert thermique M3 pour les flancs",
            quantity=28,
            material="Laiton",
            reference="M3",
            notes=(
                "Deux inserts par plaque de jonction."
            ),
        ),
        BOMItem(
            category="Structure de borne",
            name="Flanc gauche",
            quantity=1,
            material="PETG ou panneau usiné",
            reference="side_panel_left.stl",
            notes=(
                "Prototype imprimé. La version finale pourra "
                "être découpée dans un panneau."
            ),
        ),
        BOMItem(
            category="Structure de borne",
            name="Flanc droit",
            quantity=1,
            material="PETG ou panneau usiné",
            reference="side_panel_right.stl",
            notes=(
                "Miroir exact du flanc gauche."
            ),
        ),
        BOMItem(
            category="Structure de borne",
            name="Sections imprimables du flanc gauche",
            quantity=6,
            material="PETG",
            reference="side_panel_left_*.stl",
            notes=(
                "Six sections constituant le flanc gauche. "
                "Les fixations seront ajoutées au sprint suivant."
            ),
        ),
        BOMItem(
            category="Structure de borne",
            name="Sections imprimables du flanc droit",
            quantity=6,
            material="PETG",
            reference="side_panel_right_*.stl",
            notes=(
                "Six sections constituant le flanc droit."
            ),
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Support arrière de l’écran",
            quantity=2,
            material="PETG",
            reference="screen_support_x2.stl",
            notes=(
                "Ajouter une protection souple sur la "
                "surface en contact avec l’écran."
            ),
        ),
        BOMItem(
            category="Protection",
            name="Mousse ou TPU adhésif",
            quantity=2,
            material="Mousse, feutre ou TPU",
            reference="",
            notes=(
                "À placer sur les supports arrière afin "
                "de protéger le capot de l’écran."
            ),
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Module de châssis avant gauche",
            quantity=1,
            material="PETG",
            reference="chassis_front_left.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Module de châssis avant droit",
            quantity=1,
            material="PETG",
            reference="chassis_front_right.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Module de châssis arrière gauche",
            quantity=1,
            material="PETG",
            reference="chassis_rear_left.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Module de châssis arrière droit",
            quantity=1,
            material="PETG",
            reference="chassis_rear_right.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Plaque de jonction horizontale",
            quantity=2,
            material="PETG",
            reference="joiner_horizontal_x2.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Plaque de jonction verticale",
            quantity=2,
            material="PETG",
            reference="joiner_vertical_x2.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Guide latéral gauche",
            quantity=2,
            material="PETG",
            reference="laptop_guide_left_x2.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Guide latéral droit",
            quantity=2,
            material="PETG",
            reference="laptop_guide_right_x2.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Butée arrière",
            quantity=2,
            material="PETG",
            reference="laptop_rear_stop_x2.stl",
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Clip de câble arrière",
            quantity=2,
            material="PETG",
            reference="cable_clip_x2.stl",
        ),
        BOMItem(
            category="Outil de calibration",
            name="Éprouvette pour inserts thermiques M3",
            quantity=1,
            material="PETG",
            reference="insert_test_coupon.stl",
            notes=(
                "À imprimer avant le châssis pour choisir "
                "le meilleur diamètre de logement."
            ),
        ),
        BOMItem(
            category="Outil de calibration",
            name="Éprouvette de passage des vis M3",
            quantity=1,
            material="PETG",
            reference="m3_screw_test_coupon.stl",
            notes=(
                "Permet de choisir le diamètre réel des "
                "trous traversants et de tester les têtes de vis."
            ),
        ),
        BOMItem(
            category="Pièce imprimée",
            name="Patin antidérapant",
            quantity=6,
            material="TPU",
            reference="tpu_pad_x6.stl",
        ),
        BOMItem(
            category="Visserie",
            name="Vis M3",
            quantity=16,
            material="Acier",
            reference="M3",
            notes="Longueur à confirmer après le premier prototype.",
        ),
        BOMItem(
            category="Visserie",
            name="Insert thermique M3",
            quantity=16,
            material="Laiton",
            reference="M3",
        ),
        BOMItem(
            category="Équipement",
            name="Ordinateur portable",
            quantity=1,
            material="",
            reference="ASUS R753UX-T4039T",
            notes="Dimensions déclarées : 415 × 275 × 32 mm.",
        ),

    ]

    write_bom(
        items,
        DOCS_DIRECTORY / "BOM.csv",
    )


def generate_print_list() -> None:
    """Génère les recommandations d’impression."""

    petg_common = {
        "material": "PETG",
        "layer_height": "0,20 mm",
        "walls": 4,
        "supports": "Non, sauf indication du trancheur",
    }

    items = [
        PrintItem(
            file_name="side_panel_joiner_x14.stl",
            part_name="Plaque de jonction de flanc",
            quantity=14,
            material="PETG",
            layer_height="0,20 mm",
            walls=5,
            infill="50 %",
            supports="Non",
            notes=(
                "Imprimer à plat, logements d’inserts "
                "orientés vers le haut."
            ),
        ),
         PrintItem(
            file_name="side_panel_left_*.stl",
            part_name=(
                "Sections imprimables du flanc gauche"
            ),
            quantity=6,
            material="PETG",
            layer_height="0,28 mm",
            walls=5,
            infill="15 %",
            supports="Non",
            notes=(
                "Imprimer chaque section à plat. "
                "Ne pas assembler définitivement avant "
                "l’ajout des fixations mécaniques."
            ),
        ),
        PrintItem(
            file_name="side_panel_right_*.stl",
            part_name=(
                "Sections imprimables du flanc droit"
            ),
            quantity=6,
            material="PETG",
            layer_height="0,28 mm",
            walls=5,
            infill="15 %",
            supports="Non",
            notes=(
                "Imprimer chaque section à plat. "
                "Vérifier que le miroir correspond au côté droit."
            ),
        ),
        PrintItem(
            file_name="screen_support_x2.stl",
            part_name="Support arrière de l’écran",
            quantity=2,
            material="PETG",
            layer_height="0,20 mm",
            walls=5,
            infill="40 %",
            supports=(
                "Probablement nécessaires sous la "
                "surface supérieure"
            ),
            notes=(
                "Imprimer les deux pièces dans la même "
                "orientation. Vérifier l’aperçu du trancheur."
            ),
        ),
        PrintItem(
            file_name="m3_screw_test_coupon.stl",
            part_name="Éprouvette de passage des vis M3",
            quantity=1,
            material="PETG",
            layer_height="0,20 mm",
            walls=4,
            infill="40 %",
            supports="Non",
            notes=(
                "Imprimer avec les mêmes réglages que "
                "les pièces mécaniques définitives."
            ),
        ),
        PrintItem(
            file_name="chassis_front_left.stl",
            part_name="Châssis avant gauche",
            quantity=1,
            infill="25 %",
            notes="Imprimer à plat.",
            **petg_common,
        ),
        PrintItem(
            file_name="chassis_front_right.stl",
            part_name="Châssis avant droit",
            quantity=1,
            infill="25 %",
            notes="Imprimer à plat.",
            **petg_common,
        ),
        PrintItem(
            file_name="chassis_rear_left.stl",
            part_name="Châssis arrière gauche",
            quantity=1,
            infill="25 %",
            notes="Imprimer à plat.",
            **petg_common,
        ),
        PrintItem(
            file_name="chassis_rear_right.stl",
            part_name="Châssis arrière droit",
            quantity=1,
            infill="25 %",
            notes="Imprimer à plat.",
            **petg_common,
        ),
        PrintItem(
            file_name="joiner_horizontal_x2.stl",
            part_name="Plaque de jonction horizontale",
            quantity=2,
            infill="40 %",
            notes="Zone mécanique fortement sollicitée.",
            **petg_common,
        ),
        PrintItem(
            file_name="joiner_vertical_x2.stl",
            part_name="Plaque de jonction verticale",
            quantity=2,
            infill="40 %",
            notes="Zone mécanique fortement sollicitée.",
            **petg_common,
        ),
        PrintItem(
            file_name="laptop_guide_left_x2.stl",
            part_name="Guide latéral gauche",
            quantity=2,
            infill="30 %",
            notes="Paroi verticale orientée vers le portable.",
            **petg_common,
        ),
        PrintItem(
            file_name="laptop_guide_right_x2.stl",
            part_name="Guide latéral droit",
            quantity=2,
            infill="30 %",
            notes="Paroi verticale orientée vers le portable.",
            **petg_common,
        ),
        PrintItem(
            file_name="laptop_rear_stop_x2.stl",
            part_name="Butée arrière",
            quantity=2,
            infill="30 %",
            notes="Imprimer sur la base.",
            **petg_common,
        ),
        PrintItem(
            file_name="cable_clip_x2.stl",
            part_name="Clip de câble",
            quantity=2,
            infill="35 %",
            notes="Utiliser au moins quatre parois.",
            **petg_common,
        ),
        PrintItem(
            file_name="tpu_pad_x6.stl",
            part_name="Patin antidérapant",
            quantity=6,
            material="TPU 95A",
            layer_height="0,20 mm",
            walls=3,
            infill="20 %",
            supports="Non",
            notes="Imprimer lentement.",
        ),
    ]

    write_print_list(
        items,
        DOCS_DIRECTORY / "print_list.csv",
    )


def generate_hardware_list() -> None:
    """Génère la liste de visserie."""

    items = [
        HardwareItem(
            name="Insert thermique M3",
            quantity=28,
            specification=(
                "M3, diamètre extérieur selon config.py"
            ),
            usage=(
                "Plaques d’assemblage des sections de flanc"
            ),
        ),
        HardwareItem(
            name="Vis M3",
            quantity=28,
            specification=(
                "M3 à tête cylindrique, longueur conseillée "
                "22 à 25 mm"
            ),
            usage=(
                "Assemblage des sections de flanc"
            ),
            notes=(
                "La longueur définitive dépend de la profondeur "
                "réelle de l’insert."
            ),
        ),
        HardwareItem(
            name="Insert thermique M3",
            quantity=2,
            specification=(
                "M3, diamètre extérieur selon config.py"
            ),
            usage="Supports arrière de l’écran",
        ),
        HardwareItem(
            name="Vis M3",
            quantity=2,
            specification="M3 à tête cylindrique",
            usage="Supports arrière de l’écran",
        ),
        HardwareItem(
            name="Insert thermique M3",
            quantity=8,
            specification="M3, diamètre extérieur selon config.py",
            usage="Assemblage des quatre modules du châssis",
        ),
        HardwareItem(
            name="Vis M3",
            quantity=8,
            specification="M3, longueur à confirmer",
            usage="Plaques de jonction du châssis",
        ),
        HardwareItem(
            name="Insert thermique M3",
            quantity=4,
            specification="M3, diamètre extérieur selon config.py",
            usage="Guides latéraux du portable",
        ),
        HardwareItem(
            name="Vis M3",
            quantity=4,
            specification="M3 à tête cylindrique",
            usage="Guides latéraux du portable",
        ),
        HardwareItem(
            name="Insert thermique M3",
            quantity=2,
            specification="M3, diamètre extérieur selon config.py",
            usage="Butées arrière du portable",
        ),
        HardwareItem(
            name="Vis M3",
            quantity=2,
            specification="M3 à tête cylindrique",
            usage="Butées arrière du portable",
        ),
        HardwareItem(
            name="Insert thermique M3",
            quantity=2,
            specification="M3, diamètre extérieur selon config.py",
            usage="Clips de câbles arrière",
        ),
        HardwareItem(
            name="Vis M3",
            quantity=2,
            specification="M3 à tête cylindrique",
            usage="Clips de câbles arrière",
        ),
    ]

    write_hardware_list(
        items,
        DOCS_DIRECTORY / "hardware.csv",
    )


def generate_assembly_guide() -> None:
    """Génère le premier guide d’assemblage."""

    steps = [
        (
            "Imprimer l’éprouvette de calibration des inserts M3. "
            "Tester les cinq logements et noter celui qui maintient "
            "correctement l’insert sans fissurer le PETG."
        ),

        (
            "Reporter le diamètre retenu dans config.py avant de "
            "générer et d’imprimer les modules définitifs du châssis."
        ),
        (
            "Imprimer l’éprouvette de passage des vis M3. "
            "Tester chaque trou avec les vis réellement utilisées "
            "et retenir le diamètre offrant un passage libre sans "
            "jeu excessif."
        ),
        (
            "Reporter le diamètre de passage retenu dans les "
            "paramètres de vis de config.py. Vérifier également "
            "que les têtes de vis entrent complètement dans les "
            "logements de 6,5 mm."
        ),
        (
            "Ouvrir les fichiers des flancs gauche et droit dans "
            "le logiciel de CAO ou le trancheur. Vérifier la "
            "silhouette générale, l’inclinaison du panel de "
            "contrôle et l’inclinaison de la zone écran."
        ),
        (
            "Ne pas lancer l’impression complète des flancs à "
            "cette étape. Ils servent d’abord à valider les "
            "dimensions générales de la borne."
        ),
        (
            "Charger les douze sections de flanc dans le "
            "trancheur et vérifier que chaque pièce tient sur "
            "le plateau d’impression."
        ),
        (
            "Placer provisoirement les six sections de chaque "
            "côté sur une surface plane afin de reconstruire "
            "la silhouette complète du flanc."
        ),
        (
            "Imprimer les quatorze plaques de jonction de flanc "
            "et installer deux inserts thermiques M3 dans chaque "
            "plaque."
        ),
        (
            "Poser les six sections du flanc gauche face extérieure "
            "contre une surface plane. Placer les sept plaques sur "
            "la face intérieure, au-dessus des différents joints."
        ),
        (
            "Engager toutes les vis du flanc gauche sans les serrer "
            "complètement. Aligner soigneusement le contour puis "
            "serrer progressivement."
        ),
        (
            "Répéter l’opération pour le flanc droit. Vérifier que "
            "les deux flancs sont parfaitement symétriques avant "
            "de poursuivre l’assemblage de la borne."
        ),
        (
            "Ne pas coller les sections entre elles. Les joints "
            "recevront des logements de vis, des inserts et des "
            "plaques de renfort pendant le prochain sprint."
        ),
        (
            "Imprimer les quatre modules du châssis et vérifier qu’ils "
            "peuvent être placés ensemble sans chevauchement."
        ),
        (
            "Installer les inserts thermiques M3 dans les bossages du "
            "châssis. Chauffer modérément l’insert et l’enfoncer bien droit."
        ),
        (
            "Assembler les quatre modules avec les deux plaques de jonction "
            "horizontales et les deux plaques verticales."
        ),
        (
            "Poser le châssis sur une surface plane puis serrer progressivement "
            "les vis. Ne pas serrer complètement un seul côté avant les autres."
        ),
        (
            "Installer les six patins TPU sous le châssis et vérifier que "
            "l’ensemble ne bascule pas."
        ),
        (
            "Placer le portable sans le fixer afin de vérifier son centrage, "
            "les dégagements et l’accès à ses connecteurs."
        ),
        (
            "Installer les guides latéraux gauche et droit. Laisser un léger "
            "jeu afin de ne pas comprimer la coque du portable."
        ),
        (
            "Installer les deux butées arrière et vérifier que le portable "
            "ne peut plus reculer."
        ),
        (
            "Installer provisoirement les deux supports arrière "
            "de l’écran. Ajouter une protection en mousse, feutre "
            "ou TPU sur chaque surface de contact."
        ),
        (
            "Ouvrir lentement l’écran du portable jusqu’à ce qu’il "
            "repose sur les deux supports. Vérifier que la pression "
            "est répartie et que le capot ne se déforme pas."
        ),
        (
            "Installer les clips de câbles puis organiser les câbles sans "
            "bloquer les grilles de ventilation."
        ),
        (
            "Retirer une dernière fois le portable, contrôler toute la "
            "visserie, puis effectuer l’installation définitive."
        ),
    ]

    write_assembly_guide(
        steps,
        DOCS_DIRECTORY / "assembly.md",
    )


def generate_documentation() -> None:
    """Génère tous les documents du projet."""

    print("")
    print("Génération de la documentation...")

    generate_bom()
    generate_print_list()
    generate_hardware_list()
    generate_assembly_guide()

    print("  - output/docs/BOM.csv")
    print("  - output/docs/print_list.csv")
    print("  - output/docs/hardware.csv")
    print("  - output/docs/assembly.md")


def main() -> None:
    """Point d’entrée principal du générateur."""

    print("OpenDock Arcade")
    print("================")
    print("")

    generate_cad_files()
    generate_documentation()

    print("")
    print("Génération terminée.")
    print("")
    print("Quantités à imprimer :")
    print("  - flanc gauche complet de référence : 1")
    print("  - sections du flanc gauche : 6")
    print("  - flanc droit complet de référence : 1")
    print("  - sections du flanc droit : 6")
    print("  - éprouvette pour inserts M3 : 1")
    print("  - éprouvette de passage des vis M3 : 1")
    print("  - module de châssis : 4 pièces")
    print("  - plaque horizontale : 2")
    print("  - plaque verticale : 2")
    print("  - guide latéral gauche : 2")
    print("  - guide latéral droit : 2")
    print("  - butée arrière : 2")
    print("  - clip de câble arrière : 2")
    print("  - patin TPU : 6")
    print("  - support arrière de l’écran : 2")
    print("  - plaque de jonction de flanc : 14")
    print("")
    print("Visserie totale actuelle :")
    print("  - vis M3 : 46")
    print("  - inserts thermiques M3 : 46")


if __name__ == "__main__":
    main()