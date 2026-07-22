from dataclasses import dataclass

@dataclass
class Laptop:

    width: float = 415
    depth: float = 275
    height: float = 32

    visible_screen_width: float = 384
    visible_screen_height: float = 217

    bezel_width: float = 415
    bezel_height: float = 258


@dataclass
class Cabinet:

    wall = 8

    base_width = 475

    base_depth = 340

    base_thickness = 6

    rail_width = 18

    rail_height = 20

    crossbar_width = 18

    fillet = 4

    clearance = 2


laptop = Laptop()

cabinet = Cabinet()