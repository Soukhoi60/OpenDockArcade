"""
Pattern utilities
"""

from typing import List, Tuple


def linear(count: int,
           spacing: float,
           start: float = 0) -> List[float]:

    return [

        start + spacing*i

        for i in range(count)

    ]


def grid(nx,
         ny,
         dx,
         dy):

    pts = []

    for ix in range(nx):

        for iy in range(ny):

            pts.append(

                (

                    ix*dx,

                    iy*dy

                )

            )

    return pts