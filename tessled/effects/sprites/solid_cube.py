# -*- coding: utf-8 -*-

""" Solid cube sprites.

    A cube that is filled in can be any size and anywhere.
"""

from ..engine import Sprite


class SolidCube(Sprite):
    """ Solid cube sprite.

        :param tuple pos:
            Position of the corner nearest the origin as (X, Y, Z).
            Note: This is not the same order as for frames!
        :param int size:
            The size of the cube in LEDs.
    """

    def __init__(self, pos=(0, 0, 0), dims=(8, 8, 8), intensity=255):
        self.pos = pos
        self.dims = dims
        self.intensity = intensity

    def step(self):
        pass

    def render(self, frame):
        frame[max(0, self.pos[0]):min(self.pos[0] + self.dims[0], 8),
            max(0, self.pos[1]):min(self.pos[1] + self.dims[1], 8),
            max(0, self.pos[2]):min(self.pos[2] + self.dims[2], 8)] = self.intensity
