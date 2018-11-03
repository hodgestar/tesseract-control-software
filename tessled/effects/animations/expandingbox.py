# -*- coding: utf-8 -*-

""" Expanding Box animation.

    Expanding cube of LEDs.
"""

import itertools

from ..engine import Animation


class ExpandingBox(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self._sizes = itertools.cycle([2, 4, 6, 8, 6, 4])

    def render(self, frame):
        size = next(self._sizes)
        small = 4-size/2
        big = small + size-1

        frame[small, small, small:big] = 255
        frame[small, small:big, small] = 255
        frame[small, big, small:big] = 255
        frame[small, small:big, big] = 255

        frame[big, small, small:big] = 255
        frame[big, small:big, small] = 255
        frame[big, big, small:big] = 255
        frame[big, small:big, big] = 255

        frame[small:big, small, small] = 255
        frame[small:big, small, big] = 255
        frame[small:big, big, small] = 255
        frame[small:big, big, big] = 255
