# -*- coding: utf-8 -*-

""" Turn on each LED one at a time pausing for input in between.

    Useful for testing LEDs.
"""

import itertools

from ..engine import Animation


class SingleLEDs(Animation):

    ANIMATION = __name__
    ARGS = {
    }
    SKIP_GENERIC_TEST = True  # requires input

    def post_init(self):
        self._pos_cycle = itertools.cycle(
            itertools.product(*[
                range(i) for i in self.fc.frame_shape
            ]))

    def render(self, frame):
        z, y, x = next(self._pos_cycle)
        raw_input("Press enter to continue.")
        frame[z, y, x] = 255
