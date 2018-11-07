# -*- coding: utf-8 -*-

""" Utilties for working with frames.

    Frames are sent from the effectbox to the simulator or real Tesseract.
"""

import numpy as np

# Fundamental constants of the Tesseract universe
# Tesseract shape (number of Z LEDs, number of Y LEDs, number of X LEDs)
FRAME_SHAPE = (8, 8, 8)
FRAME_DTYPE = np.uint8


class FrameConstants(object):
    """ Holder for frame constants.

        :param int fps:
            Frames per second.
        :param str ttype:
            Either "simulator" if drawing to the simulator or
            "tesseract" if drawing to the real tesseract.
    """

    def __init__(self, fps=10, ttype="simulator"):
        assert ttype in ("simulator", "tesseract"), (
            "ttype must be one of 'simulator' or 'tesseract'")
        self.fps = fps
        self.ttype = ttype
        self.frame_shape = FRAME_SHAPE
        self.frame_dtype = FRAME_DTYPE
        self.layers = FRAME_SHAPE[0]

    def empty_frame(self):
        """ Return an numpy array for frame. """
        return np.zeros(self.frame_shape, dtype=self.frame_dtype)

    def virtual_to_physical(self, virt_frame):
        """ Transform a virtual frame into a phyiscal one. """
        # this is the identity operation for now -- it may change later
        return virt_frame
