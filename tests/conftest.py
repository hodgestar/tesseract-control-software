# -*- coding: utf-8 -*-

""" Configuration for pytest. """

import sys

from .fakes import spidev_fake, wiringpi_fake


sys.modules['spidev'] = spidev_fake()
sys.modules['wiringpi'] = wiringpi_fake()
