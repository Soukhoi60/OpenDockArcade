"""
OpenDock Arcade
Parametric arcade cabinet side panels
"""

from __future__ import annotations

import math
from typing import Literal

import cadquery as cq

from config import cabinet


PanelSide = Literal["left", "right"]


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
        """Vérifie les paramètres essentiels avant la construction."""

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

        # L’écran monte et recule vers l’arrière.
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

        points = [
            # Bas avant.
            (
                0.0,
                0.0,
            ),

            # Bas arrière.
            (
                cabinet.side_panel_depth,
                0.0,
            ),

            # Sommet arrière.
            (
                cabinet.side_panel_depth,
                cabinet.side_panel_height,
            ),

            # Sommet avant.
            (
                top_front_x,
                cabinet.side_panel_height,
            ),

            # Partie supérieure de la zone écran.
            (
                screen_top_x,
                screen_top_z,
            ),

            # Partie inférieure de la zone écran.
            (
                screen_bottom_x,
                screen_bottom_z,
            ),

            # Arrière du panel de contrôle.
            (
                control_rear_x,
                control_rear_z,
            ),

            # Nez avant du panel de contrôle.
            (
                control_front_x,
                control_front_z,
            ),
        ]

        return points

    def _build_raw_panel(self) -> cq.Workplane:
        """Construit le flanc sans arrondis."""

        points = self._profile_points()

        panel = (
            cq.Workplane("XZ")
            .polyline(points)
            .close()
            .extrude(
                cabinet.side_panel_thickness
            )
        )

        return panel

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

        front_x = 0.0
        front_z = (
            cabinet.side_panel_control_front_height
        )

        try:
            return (
                self._nearest_profile_edge(
                    panel,
                    front_x,
                    front_z,
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

        points = self._profile_points()
        top_front_x, top_front_z = points[3]

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
        """
        Oriente la pièce selon le côté demandé.

        Le flanc gauche est extrudé dans le sens positif de Y.
        Le flanc droit est son miroir exact.
        """

        if self.side == "left":
            return panel

        return panel.mirror(
            mirrorPlane="XZ"
        )

    def build(self) -> cq.Workplane:
        """Construit le flanc complet."""

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

        return panel.clean()