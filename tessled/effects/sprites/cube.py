# -*- coding: utf-8 -*-

""" Cube sprites.

    A cube that can be any size and anywhere.
"""

from ..engine import Sprite


class Cube(Sprite):
    """ Cube sprite.

        :param tuple pos:
            Position of the corner nearest the origin as (X, Y, Z).
            Note: This is not the same order as for frames!
        :param int size:
            The size of the cube in LEDs.
    """

    def __init__(self, pos=(0, 0, 0), size=4, intensity=255):
        self.pos = pos
        self.size = size
        self.intensity = intensity

    def step(self):
        pass

    def render(self, frame):
        sx, sy, sz = self.pos  # small values
        inc = self.size - 1
        bx, by, bz = sx + inc, sy + inc, sz + inc  # big values
        intensity = self.intensity

        frame[sz, sy, sx:bx] = intensity
        frame[sz, sy:by, sx] = intensity
        frame[sz, by, sx:bx] = intensity
        frame[sz, sy:by, bx] = intensity

        frame[bz, sy, sx:bx] = intensity
        frame[bz, sy:by, sx] = intensity
        frame[bz, by, sx:bx] = intensity
        frame[bz, sy:by, bx] = intensity

        frame[sz:bz, sy, sx] = intensity
        frame[sz:bz, sy, bx] = intensity
        frame[sz:bz, by, sx] = intensity
        frame[sz:bz, by, bx] = intensity
