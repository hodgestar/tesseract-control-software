# -*- coding: utf-8 -*-

""" FolText animation.

    Displays the text "Festival of Light" and scrolls it across the
    tesseract.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from ..engine import Animation
from ...resources import resource_filename


class FolText(Animation):

    ANIMATION = __name__
    ARGS = {
    }

    def post_init(self):
        text = "FESTIVAL OF LIGHT"
        self._x = -8

        font = ImageFont.truetype(resource_filename("vera.ttf"), size=8)
        w, h = font.getsize(text)
        image = Image.new("1", size=(w + 8, 8), color=0)
        draw = ImageDraw.Draw(image)
        draw.text((0, -1), text, font=font, fill=255)
        self._text = np.asarray(image)
        self._text = self._text[::-1, :]
        self._text = self._text * 255

    def render(self, frame):
        if self._x < self._text.shape[1] - 8:
            self._x += 1
        else:
            self._x = -8
        x_min = max(self._x, 0)
        x_max = self._x + 8
        x_diff = x_max - x_min
        frame[:, (8-x_diff):8, 0] = self._text[0:8, x_min:x_max]
