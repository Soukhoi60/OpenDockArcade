import cadquery as cq


def rounded_box(length, width, height, radius):

    box = (
        cq.Workplane("XY")
        .box(length, width, height, centered=(True, True, False))
        .edges("|Z")
        .fillet(radius)
    )

    return box


def cylinder(diameter, height):

    return (
        cq.Workplane("XY")
        .circle(diameter / 2)
        .extrude(height)
    )


def hole(workplane, diameter, depth):

    return workplane.hole(diameter, depth)