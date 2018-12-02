# -*- coding: utf-8 -*-

""" Test animation.

    Powers on selected LEDs for testing.
"""

from ..engine import Animation


class Test(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        pass

    def render(self, frame):
        frame[:, :, :] = 126
