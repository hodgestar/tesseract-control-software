# -*- coding: utf-8 -*-

""" Engine and base classes for applying effects. """

import random

import click


class EffectEngine(object):
    """ Engine for applying effects.

        Parameters
        ----------
        fc : FrameConstants
            The constants defining the earthstar.
        tick : float
            Time step between frames.
        transition : float
            Time between animation transitions.
    """

    def __init__(self, fc, tick, transition=60):
        self._animation_types = {}
        self._frame_constants = fc
        self._animation_layers = [
            'background', 'default', 'foreground',
        ]
        self._animations = dict((k, []) for k in self._animation_layers)
        self._tick = tick
        self._transition_time = transition
        # do first transition straight away
        self._next_transition = 0

    def add_animation_type(self, animation_cls):
        self._animation_types[animation_cls.ANIMATION] = animation_cls

    def add_default_animation_types(self):
        from .animations import DEFAULT_ANIMATIONS
        for animation_cls in DEFAULT_ANIMATIONS:
            self.add_animation_type(animation_cls)

    def add_animation(self, name, layer=None, **kw):
        if layer is None:
            layer = "default"
        animation_cls = self._animation_types[name]
        animation = animation_cls(self._frame_constants, **kw)
        self._animations[layer].append(animation)

    def _is_valid_new_animation(self, name, layer):
        if len(self._animation_types) <= 1:
            return True
        if len(self._animations[layer]) != 1:
            return True
        return self._animations[layer][0].ANIMATION != name

    def set_random_animation(self, layer=None):
        if layer is None:
            layer = "default"
        while True:
            name = random.choice(self._animation_types.keys())
            if self._is_valid_new_animation(name, layer):
                break
        click.echo("New animation: {!r}".format(name))
        del self._animations[layer][:]
        self.add_animation(name, layer=layer)

    def set_next_transition(self, seconds):
        self._next_transition = seconds

    def next_frame(self):
        self._next_transition -= self._tick
        if self._next_transition <= 0:
            self.set_next_transition(self._transition_time)
            self.set_random_animation()
        frame = self._frame_constants.empty_frame()
        for layer in self._animation_layers:
            for animation in self._animations[layer][:]:
                animation.render(frame)
                if animation.done():
                    self._animations[layer].remove(animation)
        return frame


class Animation(object):
    """ Base animation class. """

    ANIMATION = "unknown"
    ARGS = {}
    SKIP_GENERIC_TEST = False

    def __init__(self, frame_constants, **kw):
        self.fc = frame_constants
        self._set_args(kw)
        self.post_init()

    def _set_args(self, kw):
        for name, argtype in self.ARGS.items():
            v = argtype(kw.pop(name, None))
            setattr(self, name, v)

    def post_init(self):
        """ Post initialization set up. """

    def done(self):
        """ Return True if the animation is finished. False otherwise. """
        return False

    def render(self, frame):
        """ Render the animation to the frame. """


class Sprite(object):
    """ Base unit class.

        A unit is simply a building block for building animations on
        top of.
    """

    def step(self):
        """ Update the unit one time step.

            Updates to unit state should happen here.
        """

    def render(self, frame):
        """ Render the unit to the given frame. """
