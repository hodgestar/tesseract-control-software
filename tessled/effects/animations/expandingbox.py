# -*- coding: utf-8 -*-

""" Expanding Box animation.

    Expanding cube of LEDs.
"""

import itertools

from ..engine import Animation
from ..sprites import Cube


class ExpandingBox(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self._sizes = itertools.cycle([2, 4, 6, 8, 6, 4])
        self._cube = Cube()

    def render(self, frame):
        size = next(self._sizes)
        self._cube.size = size
        small = 4 - size / 2
        self._cube.pos = (small, small, small)
        self._cube.render(frame)
