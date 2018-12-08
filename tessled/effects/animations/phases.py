# -*- coding: utf-8 -*-

""" Phases animation.

    Lines moving in and out of phase.
"""

# -*- coding: utf-8 -*-

""" Large simple animations
"""

import random
from ..engine import Animation
from ..sprites import SolidCube


class Swipe:

    def __init__(self, line, speed):
        self.x = 0.0
        self.y = line
        self.z = 3.0
        self.line = line
        self.speed = speed
        self.pos = 0
        self.max = 7.0
        self.min = -1.0
        self.reset = False
        self.state = self.up

    def next(self):
        return self.state()

    def up(self):
        return self.step(0, self.line, -1, 0, 0, 1)

    def step(self, new_x, new_y, new_z, step_x, step_y, step_z):
        if self.reset:
            self.x = new_x
            self.y = new_y
            self.z = new_z
            self.reset = False
        self.pos += 1
        if self.pos > (self.speed):
            self.x += step_x
            self.y += step_y
            self.z += step_z
            self.pos = 0
        if self.x < self.min or self.x > self.max:
            self.reset = True
        if self.y < self.min or self.y > self.max:
            self.reset = True
        if self.z < self.min or self.z > self.max:
            self.reset = True
        if -1 < self.z < 0:
            self.z = 0
        return int(self.x), int(self.y), int(self.z)


class Phases(Animation):

    ANIMATION = __name__ + ".swipe"
    ARGS = {
    }

    def post_init(self):
        self._lines = [SolidCube(dims=(8, 1, 2)), SolidCube(dims=(8, 1, 2)),
                       SolidCube(dims=(8, 1, 2)), SolidCube(dims=(8, 1, 2)),
                       SolidCube(dims=(8, 1, 2)), SolidCube(dims=(8, 1, 2)),
                       SolidCube(dims=(8, 1, 2)), SolidCube(dims=(8, 1, 2)),]
        self._path = [Swipe(0, 4), Swipe(1, 3), Swipe(2, 2),
                      Swipe(3, 1), Swipe(4, 1), Swipe(5, 2),
                      Swipe(6, 3), Swipe(7, 4)]

    def render(self, frame):
        frames = [self.fc.empty_frame(), self.fc.empty_frame(),
                  self.fc.empty_frame(), self.fc.empty_frame(),
                  self.fc.empty_frame(), self.fc.empty_frame(),
                  self.fc.empty_frame(), self.fc.empty_frame(),]
        for i in range(8):
            self._lines[i].pos = self._path[i].next()
            self._lines[i].render(frames[i])
        frame[:, 0:1, :] = frames[0][:, 0:1, :]
        frame[:, 1:2, :] = frames[1][:, 1:2, :]
        frame[:, 2:3, :] = frames[2][:, 2:3, :]
        frame[:, 3:4, :] = frames[3][:, 3:4, :]
        frame[:, 4:5, :] = frames[4][:, 4:5, :]
        frame[:, 5:6, :] = frames[5][:, 5:6, :]
        frame[:, 6:7, :] = frames[6][:, 6:7, :]
        frame[:, 7:8, :] = frames[7][:, 7:8, :]
