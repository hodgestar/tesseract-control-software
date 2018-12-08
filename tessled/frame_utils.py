# -*- coding: utf-8 -*-

""" Utilties for working with frames.

    Frames are sent from the effectbox to the simulator or real Tesseract.
"""

import numpy as np

# Fundamental constants of the Tesseract universe
# Tesseract shape (number of Z LEDs, number of Y LEDs, number of X LEDs)
FRAME_SHAPE = (8, 8, 8)
FRAME_DTYPE = np.uint8


def simulator_virtual_to_physical(virt_frame):
    """ Convert virtual frame to physical frame for the simulator. """
    return virt_frame


def tesseract_virtual_to_physical(virt_frame):
    """ Convert virtual frame to physical frame for the simulator. """
    return virt_frame[::-1, ::-1, :]


def minicube_virtual_to_physical(virt_frame):
    """ Convert virtual frame to physical frame for the simulator. """
    return virt_frame[::-1, :, :]


class FrameConstants(object):
    """ Holder for frame constants.

        :param int fps:
            Frames per second.
        :param str ttype:
            Either "simulator" if drawing to the simulator or
            "tesseract" if drawing to the real tesseract.
    """

    TESSERACT_TYPES = {
        "simulator": simulator_virtual_to_physical,
        "tesseract": tesseract_virtual_to_physical,
        "minicube": minicube_virtual_to_physical,
    }

    def __init__(self, fps=10, ttype="simulator"):
        assert ttype in self.TESSERACT_TYPES, (
            "ttype must be one of: ".join(sorted(self.TESSERACT_TYPES.keys())))
        self.fps = fps
        self.ttype = ttype
        self.frame_shape = FRAME_SHAPE
        self.frame_dtype = FRAME_DTYPE
        self.layers = FRAME_SHAPE[0]
        self.virtual_to_physical = self.TESSERACT_TYPES[ttype]

    def empty_frame(self):
        """ Return an numpy array for frame. """
        return np.zeros(self.frame_shape, dtype=self.frame_dtype)
