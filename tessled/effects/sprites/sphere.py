# -*- coding: utf-8 -*-

""" Sphere sprite.
"""

import numpy as np

from ..engine import Sprite


class Sphere(Sprite):
    """ Sphere sprite.

        :param tuple pos:
            Position of the centre of the sphere.
        :param float radius:
            The radius of the sphere.
        :param int intensity:
            The intensity of the sphere. An integer from 0 (darkest)
            to 255 (brightest).
        :param float sharpness:
            Measure of how sharply the sphere is rendered.

        Note: The integer position coordinates mark the grid intersections
        *between* LEDs. The centres of LEDs are given by half-integer
        coordinates.
    """

    _GRID = np.mgrid[0.5:8:1, 0.5:8:1, 0.5:8:1].transpose(1, 2, 3, 0)

    def __init__(self, pos=(4, 4, 4), radius=1, intensity=255, sharpness=1):
        self.pos = pos
        self.radius = radius
        self.intensity = intensity
        self.sharpness = sharpness

    def step(self):
        pass

    def render(self, frame):
        dp = self._GRID - np.array(self.pos)
        dr = np.sqrt(np.sum(dp ** 2, -1)) - self.radius
        dr = 1 - self.sharpness * np.abs(dr)
        dr[dr < 0] = 0
        frame[:] = np.maximum(frame, dr * self.intensity)
