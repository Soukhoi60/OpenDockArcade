"""
OpenDock Arcade
Parametric arcade cabinet side panels
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal

import cadquery as cq

from config import cabinet


PanelSide = Literal["left", "right"]


@dataclass(frozen=True)
class PanelSection:
    """Zone rectangulaire utilisée pour découper un flanc."""

    name: str
    x_min: float
    x_max: float
    z_min: float
    z_max: float

@dataclass(frozen=True)
class PanelJoint:
    """
    Joint mécanique entre deux sections.

    orientation peut valoir :

    - horizontal : les deux vis sont réparties sur X ;
    - vertical : les deux vis sont réparties sur Z.
    """

    name: str
    center_x: float
    center_z: float
    orientation: Literal[
        "horizontal",
        "vertical",
    ]

class SidePanel:
    """
    Flanc paramétrique de la borne OpenDock Arcade.

    Repère utilisé :

    - X : profondeur, de l’avant vers l’arrière ;
    - Y : épaisseur du flanc ;
    - Z : hauteur.

    Le profil est construit sur le plan XZ puis extrudé suivant Y.
    """

    def __init__(
        self,
        side: PanelSide,
    ) -> None:
        if side not in ("left", "right"):
            raise ValueError(
                "side doit être 'left' ou 'right'."
            )

        self.side = side

    def _validate_parameters(self) -> None:
        """Vérifie les paramètres avant la construction."""

        if cabinet.side_panel_thickness <= 0:
            raise ValueError(
                "side_panel_thickness doit être supérieur à zéro."
            )

        if cabinet.side_panel_height <= 0:
            raise ValueError(
                "side_panel_height doit être supérieur à zéro."
            )

        if cabinet.side_panel_depth <= 0:
            raise ValueError(
                "side_panel_depth doit être supérieur à zéro."
            )

        if not (
            0.0
            < cabinet.side_panel_control_angle
            < 45.0
        ):
            raise ValueError(
                "side_panel_control_angle doit être compris "
                "entre 0 et 45 degrés."
            )

        if not (
            45.0
            < cabinet.side_panel_screen_angle
            < 90.0
        ):
            raise ValueError(
                "side_panel_screen_angle doit être compris "
                "entre 45 et 90 degrés."
            )

        if (
            cabinet.side_panel_screen_bottom_height
            <= cabinet.side_panel_control_front_height
        ):
            raise ValueError(
                "La zone écran doit commencer au-dessus "
                "du panel de contrôle."
            )

        if (
            cabinet.side_panel_screen_top_height
            <= cabinet.side_panel_screen_bottom_height
        ):
            raise ValueError(
                "La hauteur supérieure de l’écran doit être "
                "au-dessus de sa hauteur inférieure."
            )

        if (
            cabinet.side_panel_screen_top_height
            >= cabinet.side_panel_height
        ):
            raise ValueError(
                "La zone écran doit rester sous le sommet "
                "du flanc."
            )

        if not (
            0.0
            < cabinet.side_panel_lower_split_height
            < cabinet.side_panel_middle_split_height
            < cabinet.side_panel_height
        ):
            raise ValueError(
                "Les hauteurs de découpe des flancs "
                "sont invalides."
            )

        if not (
            0.0
            < cabinet.side_panel_main_split_x
            < cabinet.side_panel_upper_split_x
            < cabinet.side_panel_depth
        ):
            raise ValueError(
                "Les positions X de découpe des flancs "
                "sont invalides."
            )

    def _profile_points(
        self,
    ) -> list[tuple[float, float]]:
        """
        Calcule les points du contour dans le plan XZ.

        Chaque tuple contient :

            (x, z)
        """

        control_angle_radians = math.radians(
            cabinet.side_panel_control_angle
        )

        screen_angle_radians = math.radians(
            cabinet.side_panel_screen_angle
        )

        control_front_x = 0.0
        control_front_z = (
            cabinet.side_panel_control_front_height
        )

        control_rear_x = (
            cabinet.side_panel_control_depth
        )

        control_rear_z = (
            control_front_z
            + math.tan(control_angle_radians)
            * cabinet.side_panel_control_depth
        )

        screen_bottom_x = control_rear_x
        screen_bottom_z = (
            cabinet.side_panel_screen_bottom_height
        )

        screen_height = (
            cabinet.side_panel_screen_top_height
            - cabinet.side_panel_screen_bottom_height
        )

        screen_horizontal_offset = (
            screen_height
            / math.tan(screen_angle_radians)
        )

        screen_top_x = (
            screen_bottom_x
            + screen_horizontal_offset
        )

        screen_top_z = (
            cabinet.side_panel_screen_top_height
        )

        top_front_x = max(
            cabinet.side_panel_top_front_x,
            screen_top_x + 15.0,
        )

        return [
            (
                0.0,
                0.0,
            ),
            (
                cabinet.side_panel_depth,
                0.0,
            ),
            (
                cabinet.side_panel_depth,
                cabinet.side_panel_height,
            ),
            (
                top_front_x,
                cabinet.side_panel_height,
            ),
            (
                screen_top_x,
                screen_top_z,
            ),
            (
                screen_bottom_x,
                screen_bottom_z,
            ),
            (
                control_rear_x,
                control_rear_z,
            ),
            (
                control_front_x,
                control_front_z,
            ),
        ]

    def _build_raw_panel(self) -> cq.Workplane:
        """Construit le flanc sans arrondis."""

        return (
            cq.Workplane("XZ")
            .polyline(
                self._profile_points()
            )
            .close()
            .extrude(
                cabinet.side_panel_thickness
            )
        )

    def _nearest_profile_edge(
        self,
        panel: cq.Workplane,
        x: float,
        z: float,
    ) -> cq.Workplane:
        """
        Sélectionne l’arête traversant l’épaisseur la plus proche
        d’un point du profil.
        """

        selector = cq.selectors.NearestToPointSelector(
            (
                x,
                cabinet.side_panel_thickness / 2.0,
                z,
            )
        )

        return panel.edges(selector)

    def _apply_front_radius(
        self,
        panel: cq.Workplane,
    ) -> cq.Workplane:
        """Arrondit le nez avant du panel de contrôle."""

        radius = cabinet.side_panel_front_radius

        if radius <= 0:
            return panel

        try:
            return (
                self._nearest_profile_edge(
                    panel,
                    0.0,
                    cabinet.side_panel_control_front_height,
                )
                .fillet(radius)
            )

        except Exception:
            print(
                "Avertissement : impossible d’appliquer "
                "l’arrondi avant du flanc."
            )

            return panel

    def _apply_top_radius(
        self,
        panel: cq.Workplane,
    ) -> cq.Workplane:
        """Arrondit l’angle supérieur avant."""

        radius = cabinet.side_panel_top_radius

        if radius <= 0:
            return panel

        top_front_x, top_front_z = (
            self._profile_points()[3]
        )

        try:
            return (
                self._nearest_profile_edge(
                    panel,
                    top_front_x,
                    top_front_z,
                )
                .fillet(radius)
            )

        except Exception:
            print(
                "Avertissement : impossible d’appliquer "
                "l’arrondi supérieur du flanc."
            )

            return panel

    def _orient_panel(
        self,
        panel: cq.Workplane,
    ) -> cq.Workplane:
        """Oriente la pièce selon le côté demandé."""

        if self.side == "left":
            return panel

        return panel.mirror(
            mirrorPlane="XZ"
        )

    def _joint_definitions(
        self,
    ) -> list[PanelJoint]:
        """
        Retourne les sept joints mécaniques d’un flanc.

        Chaque joint utilise une plaque à deux inserts.
        """

        lower_z = (
            cabinet.side_panel_lower_split_height
        )

        middle_z = (
            cabinet.side_panel_middle_split_height
        )

        main_x = (
            cabinet.side_panel_main_split_x
        )

        upper_x = (
            cabinet.side_panel_upper_split_x
        )

        depth = cabinet.side_panel_depth

        return [
            # Séparation verticale des sections basses.
            PanelJoint(
                name="lower_vertical",
                center_x=main_x,
                center_z=lower_z / 2.0,
                orientation="horizontal",
            ),

            # Séparation verticale des sections centrales.
            PanelJoint(
                name="middle_vertical",
                center_x=main_x,
                center_z=(
                    lower_z
                    + middle_z
                ) / 2.0,
                orientation="horizontal",
            ),

            # Séparation verticale des sections supérieures.
            PanelJoint(
                name="upper_vertical",
                center_x=upper_x,
                center_z=(
                    middle_z
                    + cabinet.side_panel_height
                ) / 2.0,
                orientation="horizontal",
            ),

            # Séparation basse, partie avant.
            PanelJoint(
                name="lower_front_horizontal",
                center_x=main_x / 2.0,
                center_z=lower_z,
                orientation="vertical",
            ),

            # Séparation basse, partie arrière.
            PanelJoint(
                name="lower_rear_horizontal",
                center_x=(
                    main_x
                    + depth
                ) / 2.0,
                center_z=lower_z,
                orientation="vertical",
            ),

            # Séparation centrale/supérieure,
            # dans la zone avant encore présente.
            PanelJoint(
                name="upper_front_horizontal",
                center_x=(
                    main_x
                    + upper_x
                ) / 2.0,
                center_z=middle_z,
                orientation="vertical",
            ),

            # Séparation centrale/supérieure arrière.
            PanelJoint(
                name="upper_rear_horizontal",
                center_x=(
                    upper_x
                    + depth
                ) / 2.0,
                center_z=middle_z,
                orientation="vertical",
            ),
        ]

    def _joint_hole_positions(
        self,
        joint: PanelJoint,
    ) -> list[tuple[float, float]]:
        """Retourne les deux trous associés à un joint."""

        offset = (
            cabinet.side_panel_joiner_hole_offset
        )

        if joint.orientation == "horizontal":
            return [
                (
                    joint.center_x - offset,
                    joint.center_z,
                ),
                (
                    joint.center_x + offset,
                    joint.center_z,
                ),
            ]

        return [
            (
                joint.center_x,
                joint.center_z - offset,
            ),
            (
                joint.center_x,
                joint.center_z + offset,
            ),
        ]

    def _make_y_cylinder(
        self,
        *,
        x: float,
        z: float,
        diameter: float,
        start_y: float,
        length: float,
        direction_y: float,
    ) -> cq.Workplane:
        """Construit un cylindre orienté suivant l’axe Y."""

        solid = cq.Solid.makeCylinder(
            diameter / 2.0,
            length,
            cq.Vector(
                x,
                start_y,
                z,
            ),
            cq.Vector(
                0.0,
                direction_y,
                0.0,
            ),
        )

        return cq.Workplane(
            obj=solid
        )

    def _cut_joiner_screw_holes(
        self,
        panel: cq.Workplane,
    ) -> cq.Workplane:
        """Découpe les trous traversants des plaques de jonction."""

        result = panel

        thickness = (
            cabinet.side_panel_thickness
        )

        for joint in self._joint_definitions():
            for x, z in self._joint_hole_positions(
                joint
            ):
                if self.side == "left":
                    hole = self._make_y_cylinder(
                        x=x,
                        z=z,
                        diameter=(
                            cabinet
                            .side_panel_joiner_screw_diameter
                        ),
                        start_y=-0.2,
                        length=thickness + 0.4,
                        direction_y=1.0,
                    )
                else:
                    hole = self._make_y_cylinder(
                        x=x,
                        z=z,
                        diameter=(
                            cabinet
                            .side_panel_joiner_screw_diameter
                        ),
                        start_y=0.2,
                        length=thickness + 0.4,
                        direction_y=-1.0,
                    )

                result = result.cut(hole)

        return result

    def _cut_joiner_head_pockets(
        self,
        panel: cq.Workplane,
    ) -> cq.Workplane:
        """
        Découpe les logements de tête sur la face extérieure.

        La plaque de jonction se trouve sur la face intérieure.
        """

        result = panel

        thickness = (
            cabinet.side_panel_thickness
        )

        pocket_depth = (
            cabinet.side_panel_joiner_screw_head_depth
        )

        for joint in self._joint_definitions():
            for x, z in self._joint_hole_positions(
                joint
            ):
                if self.side == "left":
                    pocket = self._make_y_cylinder(
                        x=x,
                        z=z,
                        diameter=(
                            cabinet
                            .side_panel_joiner_screw_head_diameter
                        ),
                        start_y=thickness + 0.1,
                        length=pocket_depth + 0.2,
                        direction_y=-1.0,
                    )
                else:
                    pocket = self._make_y_cylinder(
                        x=x,
                        z=z,
                        diameter=(
                            cabinet
                            .side_panel_joiner_screw_head_diameter
                        ),
                        start_y=-thickness - 0.1,
                        length=pocket_depth + 0.2,
                        direction_y=1.0,
                    )

                result = result.cut(pocket)

        return result
    def _section_definitions(
        self,
    ) -> list[PanelSection]:
        """Retourne les six zones imprimables du flanc."""

        depth = cabinet.side_panel_depth
        height = cabinet.side_panel_height

        lower_z = (
            cabinet.side_panel_lower_split_height
        )

        middle_z = (
            cabinet.side_panel_middle_split_height
        )

        main_x = (
            cabinet.side_panel_main_split_x
        )

        upper_x = (
            cabinet.side_panel_upper_split_x
        )

        return [
            PanelSection(
                name="lower_front",
                x_min=0.0,
                x_max=main_x,
                z_min=0.0,
                z_max=lower_z,
            ),
            PanelSection(
                name="lower_rear",
                x_min=main_x,
                x_max=depth,
                z_min=0.0,
                z_max=lower_z,
            ),
            PanelSection(
                name="middle_front",
                x_min=0.0,
                x_max=main_x,
                z_min=lower_z,
                z_max=middle_z,
            ),
            PanelSection(
                name="middle_rear",
                x_min=main_x,
                x_max=depth,
                z_min=lower_z,
                z_max=middle_z,
            ),
            PanelSection(
                name="upper_front",
                x_min=main_x,
                x_max=upper_x,
                z_min=middle_z,
                z_max=height,
            ),
            PanelSection(
                name="upper_rear",
                x_min=upper_x,
                x_max=depth,
                z_min=middle_z,
                z_max=height,
            ),
        ]

    def _build_section_cutter(
        self,
        section: PanelSection,
    ) -> cq.Workplane:
        """
        Construit le volume utilisé pour extraire une section.

        Un très léger chevauchement évite les erreurs numériques
        sur les frontières exactes.
        """

        overlap = (
            cabinet.side_panel_section_overlap
        )

        x_min = section.x_min - overlap
        x_max = section.x_max + overlap

        z_min = section.z_min - overlap
        z_max = section.z_max + overlap

        width = x_max - x_min
        height = z_max - z_min

        cutter_y_size = (
            cabinet.side_panel_thickness
            * 4.0
        )

        return (
            cq.Workplane("XY")
            .box(
                width,
                cutter_y_size,
                height,
                centered=(
                    False,
                    True,
                    False,
                ),
            )
            .translate(
                (
                    x_min,
                    0.0,
                    z_min,
                )
            )
        )

    def _move_section_to_origin(
        self,
        section_model: cq.Workplane,
    ) -> cq.Workplane:
        """
        Place une section à plat sur le plan XY.

        Dans le flanc complet :

        - X correspond à la profondeur ;
        - Y correspond à l’épaisseur ;
        - Z correspond à la hauteur.

        Une rotation de 90 degrés autour de X place
        l’épaisseur de la pièce sur l’axe Z, comme attendu
        par un trancheur.
        """

        flat_section = section_model.rotate(
            (
                0.0,
                0.0,
                0.0,
            ),
            (
                1.0,
                0.0,
                0.0,
            ),
            90.0,
        )

        bounding_box = (
            flat_section
            .val()
            .BoundingBox()
        )

        return flat_section.translate(
            (
                -bounding_box.xmin,
                -bounding_box.ymin,
                -bounding_box.zmin,
            )
        )
    def build(self) -> cq.Workplane:
        """Construit le flanc complet avec ses fixations."""

        self._validate_parameters()

        panel = self._build_raw_panel()

        panel = self._apply_front_radius(
            panel
        )

        panel = self._apply_top_radius(
            panel
        )

        panel = self._orient_panel(
            panel
        )

        panel = self._cut_joiner_screw_holes(
            panel
        )

        panel = self._cut_joiner_head_pockets(
            panel
        )

        return panel.clean()

    def build_printable_sections(
        self,
    ) -> dict[str, cq.Workplane]:
        """
        Découpe le flanc en six sections imprimables.

        Les sections sont déplacées individuellement vers
        l’origine pour faciliter leur utilisation.
        """

        full_panel = self.build()

        sections: dict[str, cq.Workplane] = {}

        for section in self._section_definitions():
            cutter = self._build_section_cutter(
                section
            )

            section_model = full_panel.intersect(
                cutter
            )

            try:
                volume = section_model.val().Volume()
            except Exception as error:
                raise RuntimeError(
                    "Impossible d’analyser la section "
                    f"{section.name}."
                ) from error

            if volume <= 0.01:
                raise RuntimeError(
                    "La section "
                    f"{section.name} est vide. "
                    "Vérifie les paramètres de découpe."
                )

            section_model = (
                self._move_section_to_origin(
                    section_model
                )
                .clean()
            )

            sections[section.name] = (
                section_model
            )

        return sections