# -*- coding: utf-8 -*-

""" Generic tests for all animations.

    These tests run against all animation classes found in
    tessled.effects.animations.*.
"""

import glob
import os

import pytest

import tessled.effects.animations as animations
from tessled.effects.engine import EffectEngine
from tessled.frame_utils import FrameConstants


def find_animations():
    pkg_folder = os.path.dirname(animations.__file__)
    pkg_modules = [
        os.path.splitext(os.path.basename(x))[0]
        for x in glob.glob(pkg_folder + "/*.py")
        if not x.endswith('/__init__.py')
    ]
    clses = [
        animations.import_animation(x) for x in pkg_modules
    ]
    clses = [
        a for a in clses if not a.SKIP_GENERIC_TEST
    ]
    return clses


ANIMATIONS = find_animations()


@pytest.mark.parametrize("animation_cls", ANIMATIONS)
@pytest.mark.timeout(2.5)  # at least 40 frames per second
def test_generates_one_hundred_frames(animation_cls):
    """ Tests that each animation can generate one hundred
        frames correctly in a reasonable amount of time.
    """
    fc = FrameConstants()
    engine = EffectEngine(fc=fc, tick=1. / 10, transition=60)
    engine.add_animation_type(animation_cls)
    for i in range(100):
        frame = engine.next_frame()
        assert frame.shape == fc.frame_shape
        assert frame.dtype == fc.frame_dtype
