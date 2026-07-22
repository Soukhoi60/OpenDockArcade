"""
OpenDock Arcade
Parametric modular lower chassis
"""

from __future__ import annotations

import cadquery as cq

from config import cabinet, laptop
from core.frame import Frame


class Chassis:
    """Châssis inférieur modulaire adapté au portable."""

    def __init__(self) -> None:
        self.pad_positions: list[tuple[float, float]] = []

    def _laptop_edges(
        self,
    ) -> tuple[float, float, float, float]:
        """Calcule les limites du portable dans le châssis."""

        chassis_front = -cabinet.base_depth / 2.0

        laptop_front = (
            chassis_front
            + cabinet.laptop_offset_front
        )

        laptop_rear = laptop_front + laptop.depth

        laptop_left = -laptop.width / 2.0
        laptop_right = laptop.width / 2.0

        return (
            laptop_left,
            laptop_right,
            laptop_front,
            laptop_rear,
        )

    def _calculate_support_positions(
        self,
    ) -> tuple[list[float], list[float]]:
        """Calcule les positions des six patins TPU."""

        (
            laptop_left,
            laptop_right,
            laptop_front,
            laptop_rear,
        ) = self._laptop_edges()

        pad_x = [
            laptop_left + cabinet.pad_offset_side,
            laptop_right - cabinet.pad_offset_side,
        ]

        pad_y = [
            laptop_front
            + cabinet.pad_offset_front_rear,

            (
                laptop_front
                + laptop_rear
            ) / 2.0,

            laptop_rear
            - cabinet.pad_offset_front_rear,
        ]

        return pad_x, pad_y

    def _add_crossbars(
        self,
        frame: Frame,
        crossbar_y: list[float],
    ) -> None:
        """Ajoute les trois traverses principales."""

        crossbar_length = (
            cabinet.base_width
            - 2.0 * cabinet.rail_width
        )

        for y in crossbar_y:
            frame.add_box(
                x=0,
                y=y,
                z=0,
                width=crossbar_length,
                depth=cabinet.crossbar_width,
                height=cabinet.base_thickness,
            )

    def _add_reinforcement_ribs(
        self,
        frame: Frame,
        crossbar_y: list[float],
    ) -> None:
        """Ajoute une nervure sous chaque traverse."""

        rib_length = (
            cabinet.base_width
            - 2.0 * cabinet.rail_width
            - 2.0 * cabinet.rib_end_margin
        )

        for y in crossbar_y:
            frame.add_box(
                x=0,
                y=y,
                z=-cabinet.rib_height + 0.2,
                width=rib_length,
                depth=cabinet.rib_width,
                height=cabinet.rib_height,
            )

    def _cut_pad_pockets(
        self,
        frame: Frame,
        pad_x: list[float],
        pad_y: list[float],
    ) -> None:
        """Découpe les six logements des patins TPU."""

        self.pad_positions = []

        pocket_z = (
            cabinet.base_thickness
            - cabinet.pad_pocket_depth
        )

        for x in pad_x:
            for y in pad_y:
                frame.cut_cylinder(
                    x=x,
                    y=y,
                    z=pocket_z,
                    diameter=cabinet.pad_diameter,
                    depth=(
                        cabinet.pad_pocket_depth
                        + 0.2
                    ),
                )

                self.pad_positions.append((x, y))

    def _joiner_boss_positions(
        self,
    ) -> list[tuple[float, float]]:
        """
        Retourne les huit emplacements des inserts.

        Deux plaques relient gauche/droite.
        Deux plaques relient avant/arrière.
        """

        half_spacing = (
            cabinet.joiner_hole_spacing / 2.0
        )

        positions: list[tuple[float, float]] = []

        # Plaque avant gauche/droite.
        positions.extend([
            (
                -half_spacing,
                cabinet.joiner_front_y,
            ),
            (
                half_spacing,
                cabinet.joiner_front_y,
            ),
        ])

        # Plaque arrière gauche/droite.
        positions.extend([
            (
                -half_spacing,
                cabinet.joiner_rear_y,
            ),
            (
                half_spacing,
                cabinet.joiner_rear_y,
            ),
        ])

        # Plaque gauche avant/arrière.
        positions.extend([
            (
                -cabinet.joiner_side_x,
                -half_spacing,
            ),
            (
                -cabinet.joiner_side_x,
                half_spacing,
            ),
        ])

        # Plaque droite avant/arrière.
        positions.extend([
            (
                cabinet.joiner_side_x,
                -half_spacing,
            ),
            (
                cabinet.joiner_side_x,
                half_spacing,
            ),
        ])

        return positions

    def _add_joiner_bosses(
        self,
        frame: Frame,
    ) -> None:
        """Ajoute les huit bossages sous le châssis."""

        boss_z = (
            -cabinet.joiner_boss_height
            + 0.2
        )

        for x, y in self._joiner_boss_positions():
            frame.add_cylinder(
                x=x,
                y=y,
                z=boss_z,
                diameter=cabinet.joiner_boss_diameter,
                height=cabinet.joiner_boss_height,
            )

    def _cut_joiner_insert_pockets(
        self,
        frame: Frame,
    ) -> None:
        """
        Découpe les logements des inserts thermiques.

        Les logements sont ouverts depuis le dessous.
        """

        pocket_z = (
            -cabinet.joiner_boss_height
            - 0.2
        )

        for x, y in self._joiner_boss_positions():
            frame.cut_cylinder(
                x=x,
                y=y,
                z=pocket_z,
                diameter=cabinet.joiner_insert_diameter,
                depth=(
                    cabinet.joiner_insert_depth
                    + 0.4
                ),
            )

    def _guide_mount_positions(
        self,
    ) -> list[tuple[float, float]]:
        """Retourne les quatre positions des guides latéraux."""

        return [
            (
                -cabinet.guide_mount_x,
                cabinet.guide_front_y,
            ),
            (
                -cabinet.guide_mount_x,
                cabinet.guide_rear_y,
            ),
            (
                cabinet.guide_mount_x,
                cabinet.guide_front_y,
            ),
            (
                cabinet.guide_mount_x,
                cabinet.guide_rear_y,
            ),
        ]

    def _add_guide_mount_bosses(
        self,
        frame: Frame,
    ) -> None:
        """Ajoute les bossages de fixation des guides."""

        boss_z = (
            -cabinet.guide_boss_height
            + 0.2
        )

        for x, y in self._guide_mount_positions():
            frame.add_cylinder(
                x=x,
                y=y,
                z=boss_z,
                diameter=cabinet.guide_boss_diameter,
                height=cabinet.guide_boss_height,
            )

    def _cut_guide_insert_pockets(
        self,
        frame: Frame,
    ) -> None:
        """Découpe les logements des inserts M3 des guides."""

        pocket_z = (
            -cabinet.guide_boss_height
            - 0.2
        )

        for x, y in self._guide_mount_positions():
            frame.cut_cylinder(
                x=x,
                y=y,
                z=pocket_z,
                diameter=cabinet.guide_insert_diameter,
                depth=(
                    cabinet.guide_insert_depth
                    + 0.4
                ),
            )

    def _rear_stop_mount_positions(
        self,
    ) -> list[tuple[float, float]]:
        """Retourne les deux positions des butées arrière."""

        return [
            (
                -cabinet.rear_stop_mount_x,
                cabinet.rear_stop_mount_y,
            ),
            (
                cabinet.rear_stop_mount_x,
                cabinet.rear_stop_mount_y,
            ),
        ]

    def _add_rear_stop_mount_bosses(
        self,
        frame: Frame,
    ) -> None:
        """Ajoute les bossages de fixation des butées arrière."""

        boss_z = (
            -cabinet.rear_stop_boss_height
            + 0.2
        )

        for x, y in self._rear_stop_mount_positions():
            frame.add_cylinder(
                x=x,
                y=y,
                z=boss_z,
                diameter=cabinet.rear_stop_boss_diameter,
                height=cabinet.rear_stop_boss_height,
            )

    def _cut_rear_stop_insert_pockets(
        self,
        frame: Frame,
    ) -> None:
        """Découpe les logements des inserts M3 des butées."""

        pocket_z = (
            -cabinet.rear_stop_boss_height
            - 0.2
        )

        for x, y in self._rear_stop_mount_positions():
            frame.cut_cylinder(
                x=x,
                y=y,
                z=pocket_z,
                diameter=cabinet.rear_stop_insert_diameter,
                depth=(
                    cabinet.rear_stop_insert_depth
                    + 0.4
                ),
            )

    def _cable_clip_mount_positions(
        self,
    ) -> list[tuple[float, float]]:
        """Retourne les deux positions des clips de câbles."""

        return [
            (
                -cabinet.cable_clip_mount_x,
                cabinet.cable_clip_mount_y,
            ),
            (
                cabinet.cable_clip_mount_x,
                cabinet.cable_clip_mount_y,
            ),
        ]

    def _add_cable_clip_mount_bosses(
        self,
        frame: Frame,
    ) -> None:
        """Ajoute les bossages de fixation des clips."""

        boss_z = (
            -cabinet.cable_clip_boss_height
            + 0.2
        )

        for x, y in self._cable_clip_mount_positions():
            frame.add_cylinder(
                x=x,
                y=y,
                z=boss_z,
                diameter=cabinet.cable_clip_boss_diameter,
                height=cabinet.cable_clip_boss_height,
            )

    def _cut_cable_clip_insert_pockets(
        self,
        frame: Frame,
    ) -> None:
        """Découpe les logements des inserts M3 des clips."""

        pocket_z = (
            -cabinet.cable_clip_boss_height
            - 0.2
        )

        for x, y in self._cable_clip_mount_positions():
            frame.cut_cylinder(
                x=x,
                y=y,
                z=pocket_z,
                diameter=cabinet.cable_clip_insert_diameter,
                depth=(
                    cabinet.cable_clip_insert_depth
                    + 0.4
                ),
            )


    def build_full(self) -> cq.Workplane:
        """Construit le châssis complet avant découpage."""

        frame = (
            Frame()
            .create_base(
                cabinet.base_width,
                cabinet.base_depth,
                cabinet.base_thickness,
            )
            .hollow(
                cabinet.rail_width
            )
        )

        pad_x, crossbar_y = (
            self._calculate_support_positions()
        )

        self._add_crossbars(
            frame,
            crossbar_y,
        )

        self._add_reinforcement_ribs(
            frame,
            crossbar_y,
        )

        self._cut_pad_pockets(
            frame,
            pad_x,
            crossbar_y,
        )

        self._add_joiner_bosses(frame)
        self._cut_joiner_insert_pockets(frame)

        self._add_guide_mount_bosses(frame)
        self._cut_guide_insert_pockets(frame)

        self._add_rear_stop_mount_bosses(frame)
        self._cut_rear_stop_insert_pockets(frame)

        self._add_cable_clip_mount_bosses(frame)
        self._cut_cable_clip_insert_pockets(frame)

        return frame.clean().build()

    def _cutting_box(
        self,
        *,
        center_x: float,
        center_y: float,
        width: float,
        depth: float,
    ) -> cq.Workplane:
        """Crée un volume servant à extraire un module."""

        total_height = (
            cabinet.base_thickness
            + cabinet.rib_height
            + cabinet.joiner_boss_height
            + 30.0
        )

        return (
            cq.Workplane("XY")
            .box(
                width,
                depth,
                total_height,
                centered=(True, True, True),
            )
            .translate(
                (
                    center_x,
                    center_y,
                    -cabinet.rib_height / 2.0,
                )
            )
        )

    def build_modules(
        self,
    ) -> dict[str, cq.Workplane]:
        """Découpe le châssis en quatre modules imprimables."""

        full_model = self.build_full()

        half_width = cabinet.base_width / 2.0
        half_depth = cabinet.base_depth / 2.0
        half_gap = cabinet.split_gap / 2.0

        module_width = half_width - half_gap
        module_depth = half_depth - half_gap

        left_center_x = (
            -cabinet.base_width / 4.0
            - half_gap / 2.0
        )

        right_center_x = (
            cabinet.base_width / 4.0
            + half_gap / 2.0
        )

        front_center_y = (
            -cabinet.base_depth / 4.0
            - half_gap / 2.0
        )

        rear_center_y = (
            cabinet.base_depth / 4.0
            + half_gap / 2.0
        )

        cutting_boxes = {
            "front_left": self._cutting_box(
                center_x=left_center_x,
                center_y=front_center_y,
                width=module_width,
                depth=module_depth,
            ),
            "front_right": self._cutting_box(
                center_x=right_center_x,
                center_y=front_center_y,
                width=module_width,
                depth=module_depth,
            ),
            "rear_left": self._cutting_box(
                center_x=left_center_x,
                center_y=rear_center_y,
                width=module_width,
                depth=module_depth,
            ),
            "rear_right": self._cutting_box(
                center_x=right_center_x,
                center_y=rear_center_y,
                width=module_width,
                depth=module_depth,
            ),
        }

        modules: dict[str, cq.Workplane] = {}

        for name, cutting_box in cutting_boxes.items():
            modules[name] = (
                full_model
                .intersect(cutting_box)
                .clean()
            )

        return modules

    def build(self) -> cq.Workplane:
        """Retourne le châssis complet."""

        return self.build_full()