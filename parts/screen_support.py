"""
OpenDock Arcade
Removable laptop screen support
"""

from __future__ import annotations

import math

import cadquery as cq

from config import cabinet


class ScreenSupport:
    """
    Support arrière amovible pour l’écran du portable.

    Le support comporte :

    - une base vissée au châssis ;
    - un bras incliné vers l’arrière ;
    - une surface supérieure de contact avec l’écran.

    La face de contact devra recevoir une petite protection
    souple afin de ne pas marquer le capot de l’écran.
    """

    def _build_base(self) -> cq.Workplane:
        """Construit la base horizontale."""

        return (
            cq.Workplane("XY")
            .box(
                cabinet.screen_support_base_width,
                cabinet.screen_support_base_depth,
                cabinet.screen_support_base_thickness,
                centered=(True, True, False),
            )
        )

    def _build_arm(self) -> cq.Workplane:
        """Construit le bras incliné vers l’arrière."""

        angle_degrees = (
            cabinet.screen_support_tilt_angle
        )

        angle_radians = math.radians(
            angle_degrees
        )

        arm_length = (
            cabinet.screen_support_arm_length
        )

        # Position du centre du bras après inclinaison.
        arm_center_y = (
            math.sin(angle_radians)
            * arm_length
            / 2.0
        )

        arm_center_z = (
            cabinet.screen_support_base_thickness
            - 1.0
            + math.cos(angle_radians)
            * arm_length
            / 2.0
        )

        arm = (
            cq.Workplane("XY")
            .box(
                cabinet.screen_support_arm_width,
                cabinet.screen_support_arm_thickness,
                arm_length,
                centered=(True, True, True),
            )
            .rotate(
                (0, 0, 0),
                (1, 0, 0),
                -angle_degrees,
            )
            .translate(
                (
                    0,
                    arm_center_y,
                    arm_center_z,
                )
            )
        )

        return arm

    def _build_contact_pad(self) -> cq.Workplane:
        """
        Construit la surface située au sommet du support.

        Cette surface est en PETG. Une protection en mousse,
        feutre ou TPU devra être ajoutée pendant l’assemblage.
        """

        angle_degrees = (
            cabinet.screen_support_tilt_angle
        )

        angle_radians = math.radians(
            angle_degrees
        )

        arm_length = (
            cabinet.screen_support_arm_length
        )

        top_y = (
            math.sin(angle_radians)
            * arm_length
        )

        top_z = (
            cabinet.screen_support_base_thickness
            - 1.0
            + math.cos(angle_radians)
            * arm_length
        )

        contact = (
            cq.Workplane("XY")
            .box(
                cabinet.screen_support_contact_width,
                cabinet.screen_support_contact_depth,
                cabinet.screen_support_contact_height,
                centered=(True, True, True),
            )
            .rotate(
                (0, 0, 0),
                (1, 0, 0),
                -angle_degrees,
            )
            .translate(
                (
                    0,
                    top_y,
                    top_z,
                )
            )
        )

        return contact

    def _cut_mounting_hole(
        self,
        support: cq.Workplane,
    ) -> cq.Workplane:
        """Découpe le trou traversant pour la vis M3."""

        screw_hole = (
            cq.Workplane("XY")
            .circle(
                cabinet.screen_support_screw_diameter
                / 2.0
            )
            .extrude(
                cabinet.screen_support_base_thickness
                + 0.4
            )
            .translate(
                (
                    0,
                    -8.0,
                    -0.2,
                )
            )
        )

        return support.cut(screw_hole)

    def _cut_screw_head_pocket(
        self,
        support: cq.Workplane,
    ) -> cq.Workplane:
        """Découpe le logement supérieur de la tête de vis."""

        pocket_start_z = (
            cabinet.screen_support_base_thickness
            - cabinet.screen_support_screw_head_depth
            - 0.1
        )

        head_pocket = (
            cq.Workplane("XY")
            .circle(
                cabinet.screen_support_screw_head_diameter
                / 2.0
            )
            .extrude(
                cabinet.screen_support_screw_head_depth
                + 0.2
            )
            .translate(
                (
                    0,
                    -8.0,
                    pocket_start_z,
                )
            )
        )

        return support.cut(head_pocket)

    def build(self) -> cq.Workplane:
        """Construit le support complet."""

        support = self._build_base()

        support = support.union(
            self._build_arm()
        )

        support = support.union(
            self._build_contact_pad()
        )

        support = self._cut_mounting_hole(
            support
        )

        support = self._cut_screw_head_pocket(
            support
        )

        return support.clean()