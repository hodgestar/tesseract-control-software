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
        self._layer = 0
        self._frame = self.fc.empty_frame()

    def render(self, frame):
        self._frame[self._layer] = 0
        self._layer = (self._layer + 1) % (self.fc.frame_shape[2])
        self._frame[self._layer] = 255
        frame[:] = self._frame
