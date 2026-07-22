from dataclasses import dataclass


@dataclass(frozen=True)
class Laptop:
    width: float = 415.0
    depth: float = 275.0
    height: float = 32.0

    visible_screen_width: float = 384.0
    visible_screen_height: float = 217.0

    bezel_width: float = 415.0
    bezel_height: float = 258.0


@dataclass(frozen=True)
class Cabinet:
    # Châssis général
    base_width: float = 475.0
    base_depth: float = 340.0
    base_thickness: float = 6.0

    rail_width: float = 18.0
    rail_height: float = 20.0
    crossbar_width: float = 22.0

    # Nervures sous les traverses
    rib_width: float = 6.0
    rib_height: float = 12.0
    rib_end_margin: float = 12.0

    # Découpage pour impression
    split_gap: float = 0.4
    split_margin: float = 5.0

    # Assemblage des quatre modules
    joiner_plate_length: float = 64.0
    joiner_plate_width: float = 24.0
    joiner_plate_thickness: float = 4.0

    joiner_hole_spacing: float = 40.0

    joiner_boss_diameter: float = 12.0
    joiner_boss_height: float = 8.0

    joiner_screw_diameter: float = 3.4
    joiner_screw_head_diameter: float = 6.5
    joiner_screw_head_depth: float = 2.2

    joiner_insert_diameter: float = 4.6
    joiner_insert_depth: float = 5.2

    # Position des plaques
    joiner_front_y: float = -110.0
    joiner_rear_y: float = 115.0
    joiner_side_x: float = 219.0

    # Guides latéraux du portable
    guide_length: float = 52.0
    guide_base_width: float = 28.0
    guide_base_thickness: float = 5.0
    guide_wall_thickness: float = 5.0
    guide_height: float = 22.0
    guide_corner_radius: float = 3.0

    guide_mount_x: float = 228.0
    guide_front_y: float = -75.0
    guide_rear_y: float = 75.0

    guide_screw_diameter: float = 3.4
    guide_screw_head_diameter: float = 6.5
    guide_screw_head_depth: float = 2.2

    guide_insert_diameter: float = 4.6
    guide_insert_depth: float = 5.2
    guide_boss_diameter: float = 12.0
    guide_boss_height: float = 8.0

    fillet: float = 4.0
    clearance: float = 2.0

    # Butées arrière du portable
    rear_stop_base_width: float = 40.0
    rear_stop_base_depth: float = 28.0
    rear_stop_base_thickness: float = 5.0

    rear_stop_wall_thickness: float = 5.0
    rear_stop_wall_height: float = 22.0

    rear_stop_mount_x: float = 150.0
    rear_stop_mount_y: float = 154.0

    rear_stop_screw_diameter: float = 3.4
    rear_stop_screw_head_diameter: float = 6.5
    rear_stop_screw_head_depth: float = 2.2

    rear_stop_insert_diameter: float = 4.6
    rear_stop_insert_depth: float = 5.2

    rear_stop_boss_diameter: float = 12.0
    rear_stop_boss_height: float = 8.0

    # Position du portable :
    # distance entre le bord avant du châssis et le portable
    laptop_offset_front: float = 35.0

    # Appuis TPU
    pad_diameter: float = 20.0
    pad_height: float = 3.0
    pad_pocket_depth: float = 2.0
    pad_offset_side: float = 35.0
    pad_offset_front_rear: float = 25.0

    # Guides latéraux
    guide_width: float = 8.0
    guide_height: float = 18.0
    guide_clearance: float = 1.0

    # Butée arrière
    rear_stop_width: float = 30.0
    rear_stop_height: float = 15.0
    rear_stop_thickness: float = 8.0

    # Visserie
    insert_m3_diameter: float = 4.6
    insert_m3_depth: float = 5.2
    screw_m3_clearance: float = 3.2


laptop = Laptop()
cabinet = Cabinet()