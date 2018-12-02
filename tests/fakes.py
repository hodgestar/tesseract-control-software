# -*- coding: utf-8 -*-

""" Fakes for hardware modules only available on the Raspberry Pi. """

from types import ModuleType


class SpiDev:
    """ A dummy SPI device. """

    def __init__(self):
        self.fake_state = {}

    def fileno(self):
        return 4

    def open(self, spibus, spidevice):
        self.fake_state.update({
            "open": True,
            "bus": spibus,
            "device": spidevice,
        })


class FakeSpidev:
    """ Holder for internal state of a fake spidev module. """

    def __init__(self):
        self.spidevs = []

    def SpiDev(self):
        dev = SpiDev()
        self.spidevs.append(dev)
        return dev


def spidev_fake():
    """ Returns a fake spidev module. """
    mod = ModuleType("spidev")
    mod.fake = FakeSpidev()
    mod.SpiDev = mod.fake.SpiDev
    return mod


class GPIO:
    """ A dummy GPIO object. """

    WPI_MODE_PINS = "__WPI_MODE_PINS__"

    OUTPUT = "__OUTPUT__"

    HIGH = 1
    LOW = 0

    def __init__(self):
        self.fake_state = {}

    def __call__(self, mode):
        self.fake_state.update({
            "mode": mode,
            "initialized": True,
        })
        return self

    def pinMode(self, pin, mode):
        self.fake_state.update({
            "pin-{}".format(pin): mode,
        })


class FakeWiringpi:
    """ Holder for internal state of a fake wiringpi module. """

    def __init__(self):
        self.GPIO = GPIO()


def wiringpi_fake():
    """ Returns a fake wiringpi module. """
    mod = ModuleType("wiringpi")
    mod.fake = FakeWiringpi()
    mod.GPIO = mod.fake.GPIO
    return mod
