# -*- coding: utf-8 -*-

""" Exploring Box animation.

    Inquisitive pair of cubes of LEDs.
"""

import random

from ..engine import Animation
from ..sprites import Cube


class SpiralPath:

    def __init__(self, margin, offset=0.0):
        steps_x = 8 - margin[0]
        steps_y = 8 - margin[1]
        self._max_z = 8 - margin[2]

        self._xy = []
        self._xy += zip([0] * steps_y, range(0, steps_y))
        self._xy += zip(range(0, steps_x), [steps_y] * steps_x)
        self._xy += zip([steps_x] * steps_y, range(steps_y - 1, -1, -1))
        self._xy += zip(range(steps_x - 1, -1, -1), [0] * steps_x)

        self._t = int(len(self._xy) * offset)

    def next(self):
        once_around = len(self._xy)
        pz = self._t // once_around
        r = self._t % once_around
        px, py = self._xy[r]
        self._t += 1
        self._t %= (self._max_z + 1) * once_around
        return (px, py, pz)


class ExploringBox(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        size1 = random.choice([2, 3, 4, 5])
        self._cube1 = Cube(size=size1)
        self._spiral_path1 = SpiralPath(
            margin=(size1, size1, size1))
        size2 = random.choice([2, 3, 4, 5])
        self._cube2 = Cube(size=size2)
        self._spiral_path2 = SpiralPath(
            margin=(size2, size2, size2),
            offset=0.5)

    def render(self, frame):
        self._cube1.pos = self._spiral_path1.next()
        self._cube1.render(frame)
        self._cube2.pos = self._spiral_path2.next()
        self._cube2.render(frame)
