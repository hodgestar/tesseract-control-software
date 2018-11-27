# -*- coding: utf-8 -*-

""" Tests for spidev_driver.
"""

import numpy as np

# these are expected to be fakes at this point
from spidev import fake as spidev_fake
from wiringpi import fake as wiringpi_fake

from tessled.spidev_driver import TLCs, pack_to_12bit, pack_to_6bit


class TestPackTo12Bit:
    def test_zeros(self):
        x = pack_to_12bit(np.array([0, 0]))
        assert np.array_equal(x, [0, 0, 0])
        assert x.dtype == np.uint8

    def test_ones(self):
        x = pack_to_12bit(np.array([4095, 4095]))
        assert np.array_equal(x, [255, 255, 255])
        assert x.dtype == np.uint8


class TestPackTo6Bit:
    def test_zeros(self):
        x = pack_to_6bit(np.array([0, 0, 0, 0]))
        assert np.array_equal(x, [0, 0, 0])
        assert x.dtype == np.uint8

    def test_ones(self):
        x = pack_to_6bit(np.array([63, 63, 63, 63]))
        assert np.array_equal(x, [255, 255, 255])
        assert x.dtype == np.uint8


class TestTLCs:
    def test_create_inverted(self):
        tlcs = TLCs(tlcs=5, gsclk=4, blank=3, vprg=5, xlat=6, dcprg=7,
                    spibus=0, spidevice=1, spispeed=500000)
        assert tlcs.n_tlcs == 5
        assert tlcs.n_outputs == 5 * 16
        assert tlcs.gsclk == 4
        assert tlcs.blank == 3
        assert tlcs.vprg == 5
        assert tlcs.xlat == 6
        assert tlcs.dcprg == 7
        assert tlcs.HIGH == 0
        assert tlcs.LOW == 1
        assert wiringpi_fake.GPIO.fake_state == {
            'initialized': True,
            'mode': '__WPI_MODE_PINS__',
            'pin-4': '__OUTPUT__',
            'pin-3': '__OUTPUT__',
            'pin-5': '__OUTPUT__',
            'pin-6': '__OUTPUT__',
            'pin-7': '__OUTPUT__',
        }
        [dev] = spidev_fake.spidevs
        assert dev.fake_state == {
            "bus": 0,
            "device": 1,
            "open": True,
        }
        assert dev.max_speed_hz == 500000
        assert dev.mode == 0b10
