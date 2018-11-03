# -*- coding: utf-8 -*-

""" PowerOn animation.

    Powers on the LEDs in columns.
"""

from ..engine import Animation


class PowerOn(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self._frame = self.fc.empty_frame()

    def render(self, frame):
        frame[:] = self._frame
