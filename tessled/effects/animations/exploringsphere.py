# -*- coding: utf-8 -*-

""" Exploring Sphere animation.

    Inquisitive sphere.
"""

import numpy as np
import time

from ..engine import Animation
from ..sprites import Sphere


class ExploringSphere(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        self._max_radius = 6
        self._hz = 0.2
        self._spheres = [
            Sphere(pos=(2, 2, 2), sharpness=0.5),
            Sphere(pos=(6, 6, 6), sharpness=0.5),
        ]

    def render(self, frame):
        t = time.time()
        r = self._max_radius * (1 + np.sin(t * self._hz * 2 * np.pi)) / 2
        for s in self._spheres:
            s.radius = r
            s.render(frame)
