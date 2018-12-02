# -*- coding: utf-8 -*-

""" Test animation.

    Powers on selected LEDs for testing.
"""

from ..engine import Animation


class PowerOn(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self.intensity = 1
        self.x = 0
        self.y = 0
        self.step = 0
        self._frame = self.fc.empty_frame()

    def render(self, frame):
        #self.intensity += 1
        #self.intensity = self.intensity % 4095
        #self.step += 1
        #import math
        #f = math.sin(self.step * 0.1)
        frame[:, :, :] = 126
        return
        self.step += 1
        if self.step > 20:
            for l in range(self.fc.frame_shape[2]):
                self._frame[l][self.x][self.y] = 0
            self.x = (self.x + 1) % 8
            self.step = 0
            for l in range(self.fc.frame_shape[2]):
                self._frame[l][self.x][self.y] = self.intensity
        frame[:] = self._frame
