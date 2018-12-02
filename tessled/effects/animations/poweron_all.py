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
        self.intensity = 1
        self._frame = self.fc.empty_frame()

    def render(self, frame):
        #self.intensity += 1
        #self.intensity = self.intensity % 4095
        for l in range(self.fc.frame_shape[2]):
            self._frame[l] = self.intensity
        frame[:] = self._frame
