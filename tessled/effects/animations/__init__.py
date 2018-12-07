# -*- coding: utf-8 -*-

""" Animations package. """

from ..engine import Animation
from .expandingbox import ExpandingBoxFast, ExpandingBoxSlow
from .exploringbox import ExploringBox
from .exploringsphere import ExploringSphere
from .foltext import FolText
from .fxyt import (
    FxytWaveY, FxytWaveXY,
    FxytRotatingPlane, FxytRotatingParabaloid,
    FxytBreather)
from .poweron import PowerOn

DEFAULT_ANIMATIONS = [
    ExpandingBoxFast,
    ExpandingBoxSlow,
    ExploringBox,
    ExploringSphere,
    FolText,
    FxytWaveXY,
    FxytWaveY,
    FxytRotatingPlane,
    FxytRotatingParabaloid,
    FxytBreather,
    PowerOn,
]


def import_animations(name):
    """ Import all animation classes from a named module. """
    fullname = "{}.{}".format(__name__, name)
    module = __import__(fullname)
    for part in fullname.split(".")[1:]:
        module = getattr(module, part)
    objs = [getattr(module, x) for x in dir(module) if not x.startswith("_")]
    objs = [x for x in objs if type(x) == type and issubclass(x, Animation)]
    objs = [x for x in objs if x is not Animation]
    return objs


def import_animation(name, subname=None):
    """ Import an animation class by module name. """
    objs = import_animations(name)
    if subname:
        objs = [x for x in objs if x.ANIMATION.endswith('.' + subname)]
    return objs[0]
