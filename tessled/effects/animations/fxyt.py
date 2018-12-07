# -*- coding: utf-8 -*-

""" Animations of the form z = f(x, y, t).
"""

import time

import numpy as np

from ..engine import Animation
from ..engine import Sprite


def frange(x=(0, 1), y=(0, 1), z=(0, 1)):
    """ Apply range attributes to a function. """
    def decorator(f):
        f.range_x = x
        f.range_y = y
        f.range_z = z
        return f
    return decorator


class Fxyt(Sprite):
    def __init__(self, f):
        self.f = f
        self.grid = np.mgrid[
            f.range_x[0]:f.range_x[1]:8j,
            f.range_y[0]:f.range_y[1]:8j]
        self.x = self.grid[0, :, :]
        self.y = self.grid[1, :, :]
        self.gridi = np.mgrid[0:8, 0:8]
        self.xi = self.gridi[0, :, :]
        self.yi = self.gridi[1, :, :]
        self.z_min = f.range_z[0]
        self.z_resize = (f.range_z[1] - f.range_z[0]) / 8.

    def render(self, frame):
        t = time.time()
        z = self.f(self.x, self.y, t)
        z = (z - self.z_min) / self.z_resize
        zi = np.floor(z).astype(np.int).clip(0, 7)
        frame[zi, self.yi, self.xi] = 255


class FxytMexicanHat(Animation):

    ANIMATION = __name__ + ".mexican_hat"
    ARGS = {
    }

    def post_init(self):
        self.fxyt = Fxyt(self.f)

    def render(self, frame):
        self.fxyt.render(frame)

    @frange(x=(-8, 8), y=(-8, 8), z=(-0.2, 0.6))
    def f(self, x, y, t):
        R = np.sqrt(x**2 + y**2) + 0.01
        A = np.sin(t)**2 + 0.01
        return A * np.sin(R) / R


class FxytWaveY(FxytMexicanHat):

    ANIMATION = __name__ + ".wavey"

    @frange(x=(-np.pi, np.pi), y=(-np.pi, np.pi), z=(-1, 1))
    def f(self, x, y, t):
        return np.sin(y + 1.5 * t)
