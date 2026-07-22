"""
OpenDock Arcade
Separate TPU support pad
"""

from __future__ import annotations

import cadquery as cq

from config import cabinet
from core.features import tpu_pad


class TPUPad:
    """Patin TPU imprimé séparément."""

    def build(self) -> cq.Workplane:
        return tpu_pad(
            diameter=cabinet.pad_diameter - 0.4,
            height=cabinet.pad_height,
        )