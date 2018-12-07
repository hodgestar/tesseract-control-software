# -*- coding: utf-8 -*-

""" Expanding Box animation.

    Expanding cube of LEDs.
"""

import itertools

from ..engine import Animation
from ..sprites import Cube


class ExpandingBoxSlow(Animation):

    ANIMATION = __name__ + ".slow"
    ARGS = {
    }
    SLOWNESS = 4

    def post_init(self):
        self._t = 0
        self._sizes = itertools.cycle([2, 4, 6, 8, 6, 4])
        self._cube = Cube()

    def render(self, frame):
        self._t = (self._t + 1) % self.SLOWNESS
        if self._t == 0:
            self._cube.size = next(self._sizes)
        small = 4 - self._cube.size / 2
        self._cube.pos = (small, small, small)
        self._cube.render(frame)


class ExpandingBoxFast(ExpandingBoxSlow):

    ANIMATION = __name__ + ".fast"
    SLOWNESS = 2
