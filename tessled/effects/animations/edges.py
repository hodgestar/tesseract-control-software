# -*- coding: utf-8 -*-

""" Large simple animations
"""

import random
from ..engine import Animation
from ..sprites import SolidCube


class Swipe:

    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.flat_step = 0.5
        self.diag = 0.33
        self.max = 8.0
        self.min = -8.0
        self.reset = True
        self.state = self.up

    def next(self):
        if self.reset:
            self.state = random.choice(
                [self._in, self.out, self.up, self.down, self.left, self.right,
                 self._in, self.out, self.up, self.down, self.left, self.right,
                 self.diag_up_left_in, self.diag_up_left_out,
                 self.diag_up_right_in, self.diag_up_right_out,
                 self.diag_down_left_in, self.diag_down_left_out,
                 self.diag_down_right_in, self.diag_down_right_out])
        return self.state()

    def up(self):
        return self.step(-8, 0, 0, self.flat_step, 0, 0)

    def down(self):
        return self.step(8, 0, 0, -self.flat_step, 0, 0)

    def left(self):
        return self.step(0, -8, 0, 0, self.flat_step, 0)

    def right(self):
        return self.step(0, 8, 0, 0, -self.flat_step, 0)

    def _in(self):
        return self.step(0, 0, -8, 0, 0, self.flat_step)

    def out(self):
        return self.step(0, 0, 8, 0, 0, -self.flat_step)

    def diag_up_left_in(self):
        return self.step(-8, -8, -8, self.diag, self.diag, self.diag)

    def diag_up_left_out(self):
        return self.step(-8, -8, 8, self.diag, self.diag, -self.diag)

    def diag_up_right_in(self):
        return self.step(-8, 8, -8, self.diag, -self.diag, self.diag)

    def diag_up_right_out(self):
        return self.step(-8, 8, 8, self.diag, -self.diag, -self.diag)

    def diag_down_left_in(self):
        return self.step(8, -8, -8, -self.diag, self.diag, self.diag)

    def diag_down_left_out(self):
        return self.step(8, -8, 8, -self.diag, self.diag, -self.diag)

    def diag_down_right_in(self):
        return self.step(8, 8, -8, -self.diag, -self.diag, self.diag)

    def diag_down_right_out(self):
        return self.step(8, 8, 8, -self.diag, -self.diag, -self.diag)

    def step(self, new_x, new_y, new_z, step_x, step_y, step_z):
        if self.reset:
            self.x = new_x
            self.y = new_y
            self.z = new_z
            self.reset = False
        self.x += step_x
        self.y += step_y
        self.z += step_z
        if self.x < self.min or self.x > self.max:
            self.reset = True
        if self.y < self.min or self.y > self.max:
            self.reset = True
        if self.z < self.min or self.z > self.max:
            self.reset = True
        return (int(self.x), int(self.y), int(self.z))


class SolidEdge(Animation):

    ANIMATION = __name__ + ".swipe"
    ARGS = {
    }

    def post_init(self):
        self._cube = SolidCube()
        self._path = Swipe()

    def render(self, frame):
        self._cube.pos = self._path.next()
        self._cube.render(frame)
