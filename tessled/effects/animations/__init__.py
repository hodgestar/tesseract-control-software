# -*- coding: utf-8 -*-

""" Animations package. """

from ..engine import Animation
from .expandingbox import ExpandingBox
from .exploringbox import ExploringBox
from .exploringsphere import ExploringSphere
from .foltext import FolText
from .poweron import PowerOn

DEFAULT_ANIMATIONS = [
    ExpandingBox,
    ExploringBox,
    ExploringSphere,
    FolText,
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


def import_animation(name):
    """ Import an animation class by module name. """
    return import_animations(name)[0]
