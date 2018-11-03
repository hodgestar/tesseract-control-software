# -*- coding: utf-8 -*-

""" Resources package. """

import pkg_resources


def resource_filename(name):
    """ Return the filename of the given resource. """
    return pkg_resources.resource_filename(__name__, name)
