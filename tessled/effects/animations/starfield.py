# -*- coding: utf-8 -*-

""" Starfield animation.

    Many LEDs that turn on and off.
"""

import numpy as np

from ..engine import Animation


class Starfield(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self.stars = [[], [], []]
        self.n = 100
        self.add_stars(self.n)

    def add_stars(self, n):
        for _ in range(n):
            for i in range(3):
                self.stars[i].append(np.random.randint(8))

    def del_stars(self, n):
        for i in range(3):
            del self.stars[i][0:n]

    def render(self, frame):
        self.del_stars(self.n / 10)
        self.add_stars(self.n / 10)
        frame[self.stars[0], self.stars[1], self.stars[2]] = 255
