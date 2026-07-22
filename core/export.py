import cadquery as cq
from cadquery import exporters
from pathlib import Path


OUTPUT = Path("output")

OUTPUT.mkdir(exist_ok=True)


def export(name, part):

    step = OUTPUT / f"{name}.step"

    stl = OUTPUT / f"{name}.stl"

    exporters.export(part, str(step))

    exporters.export(part, str(stl))

    print(f"Export : {name}")