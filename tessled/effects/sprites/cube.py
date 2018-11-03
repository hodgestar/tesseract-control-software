# -*- coding: utf-8 -*-

""" Cube sprites.

    A cube that can be any size divisible by 2 and anywhere.
"""

from ..engine import Sprite


class Cube(Sprite):

    def __init__(self, pos=(0, 0, 0), size=4):
        self.pos = pos
        self.size = size

    def step(self):
        pass

    def render(self, frame):
        sx, sy, sz = self.pos  # small values
        inc = self.size - 1
        bx, by, bz = sx + inc, sy + inc, sz + inc  # big values

        frame[sz, sy, sx:bx] = 255
        frame[sz, sy:by, sx] = 255
        frame[sz, by, sx:bx] = 255
        frame[sz, sy:by, bx] = 255

        frame[bz, sy, sx:bx] = 255
        frame[bz, sy:by, sx] = 255
        frame[bz, by, sx:bx] = 255
        frame[bz, sy:by, bx] = 255

        frame[sz:bz, sy, sx] = 255
        frame[sz:bz, sy, bx] = 255
        frame[sz:bz, by, sx] = 255
        frame[sz:bz, by, bx] = 255
