# -*- coding: utf-8 -*-

""" Effect argument types. """


class StrArg(object):
    def __init__(self, allow_null=False):
        self._allow_null = allow_null

    def __call__(self, v):
        if self._allow_null and v is None:
            return None
        return str(v)


class DictArg(object):
    def __init__(self, allow_null=False):
        self._allow_null = allow_null

    def __call__(self, v):
        if self._allow_null and v is None:
            return v
        assert isinstance(v, dict)
        return v


class IntArg(object):
    def __init__(self, default, min=None, max=None):
        self._default = default
        self._min = min
        self._max = max

    def __call__(self, v):
        try:
            v = int(v)
        except Exception:
            return self._default
        if self._min is not None:
            v = max(v, self._min)
        if self._max is not None:
            v = min(v, self._max)
        return v


class FloatArg(object):
    def __init__(self, default, min=None, max=None):
        self._default = default
        self._min = min
        self._max = max

    def __call__(self, v):
        try:
            v = float(v)
        except Exception:
            return self._default
        if self._min is not None:
            v = max(v, self._min)
        if self._max is not None:
            v = min(v, self._max)
        return v
