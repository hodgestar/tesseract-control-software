# -*- coding: utf-8 -*-

""" Tesseract LED driver that uses spidev to control the TLC5940 chips.

    It assumes that there are 5 TLC chips arranged as follows:

    * Chips 1-4 control the 64 ground lines of the Tesseract, control
      which of the 64 LEDs in a given layer are grounded.

    * The first 8 lines from the 5th chip control which layer is powered.

    The driver receives frames from ZeroMQ and continual cycles through
    the layers until a new frame is received via ZeroMQ.

    The frame layout is described in tessled.effectbox.
"""

import os

import click
import numpy as np
import zmq

import wiringpi
import spidev

from . import frame_utils


def pack_to_12bit(values):
    """ Pack an array of integers to an array of 12-bit values
        each stored in one and half bytes.

        Each set of two values is stored as three bytes::

            [V_00 .. V_07] [V_08 .. V_0B, V_10 .. V13] [V_14 .. V_1B]

        Currently timed at ~10us for 80 values.
    """
    values = values % 4096  # clamp to 0 to 4095 (i.e. 12 bit)
    v_0, v_1 = values[0::2], values[1::2]
    b = np.zeros(3 * len(values) / 2, dtype=np.uint8)
    b[0::3] = (v_0 >> 4)
    b[1::3] = ((v_0 % 16) << 4) + (v_1 >> 8)
    b[2::3] = (v_1 % 256)
    return b


def pack_to_6bit(values):
    """ Pack an array of integers to an array of 6-bit values
        each stored in three quarters of a byte.

        Each set of four values is stored as three bytes::

            [V_00 .. V_05, V_10 .. V_11] [V_12 .. V_15, V_20 .. V_23]
            [V_24 .. V_25, V_30 .. V_35]

        Currently timed at ~15us for 80 values.
    """
    values = values % 64  # clamp to 0 to 63 (i.e. 6 bit)
    v_0, v_1, v_2, v_3 = values[0::4], values[1::4], values[2::4], values[3::4]
    b = np.zeros(3 * len(values) / 4, dtype=np.uint8)
    b[0::3] = (v_0 << 2) + (v_1 >> 4)
    b[1::3] = ((v_1 % 16) << 4) + (v_2 >> 2)
    b[2::3] = ((v_2 % 4) << 6) + (v_3)
    return b


class TLCs(object):
    """ Object representing a chain of TLCs and controlling them using
        wiringpi (for general GPIO) and spidev (for clocking data into
        the TLC chips using SPI).

        :param int tlcs:
            The number of TLC chips connected in series.
        :param int blank:
            The (wiringpi) pin number connected to the TLC BLANK line.
        :param int vprg:
            The (wiringpi) pin number connected to the TLC VPRG line.
        :param int xlat:
            The (wiringpi) pin number connected to the TLC XLAT line.
        :param int dcprg:
            The (wiringpi) pin number connected to the TLC DCPRG line.
        :param int spibus:
            The number of the SPI bus to use. Default: 0.
        :param int spidevice:
            The number of the SPI device to use. Default: 0.
        :param int spispeed:
            The SPI maximum speed in Hz. Default: 500 kHz.
        :param bool inverted:
            Whether the signal logic should be inverted (for both the SPI
            signals and the GPIO controlled pins). Default: True.

        Inspired heavily by
        https://github.com/eflukx/enlightenPi/blob/master/TLC5940.py.
    """
    def __init__(
            self, tlcs, blank, vprg, xlat, dcprg,
            spibus=0, spidevice=0, spispeed=500000, inverted=True):
        self.n_tlcs = tlcs
        self.n_outputs = self.n_tlcs * 16  # 16 outputs per TLC
        self.blank = blank
        self.vprg = vprg
        self.xlat = xlat
        self.dcprg = dcprg

        # setup SPI
        self.spi = spidev.SpiDev()
        self.spi.open(spibus, spidevice)
        self.spi_fd = self.spi.fileno()
        self.spi.max_speed_hz = spispeed
        if inverted:
            self.spi.mode = 0b10  # invert clock signal

        # setup GPIO pins
        self.gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
        self.gpio.pinMode(self.blank, self.gpio.OUTPUT)
        self.gpio.pinMode(self.vprg, self.gpio.OUTPUT)
        self.gpio.pinMode(self.xlat, self.gpio.OUTPUT)
        self.gpio.pinMode(self.dcprg, self.gpio.OUTPUT)

        if inverted:
            self.HIGH = self.gpio.LOW
            self.LOW = self.gpio.HIGH
        else:
            self.HIGH = self.gpio.HIGH
            self.LOW = self.gpio.LOW

    def init_tlcs(self):
        """ Initialize the TLCs."""
        self.gpio.digitalWrite(self.dcprg, self.LOW)
        self.gpio.digitalWrite(self.vprg, self.HIGH)
        self.gpio.digitalWrite(self.xlat, self.LOW)
        self.gpio.digitalWrite(self.blank, self.HIGH)
        self.gpio.digitalWrite(self.vprg, self.LOW)

    def write_dc(self, dc_values):
        """ Write the dot clock (DC) levels.

            :param numpy.array dc_values:
                A numpy array with the dot clock values for each TLC output.
                Each value must be in the range 0-63 (inclusive).

            Values are written to the TLCs in reverse order (since each value
            is clocked through to the next input).
        """
        dc_buffer = pack_to_6bit(dc_values[::-1])
        dc_buffer = np.bitwise_not(dc_buffer)
        self.gpio.digitalWrite(self.dcprg, self.HIGH)
        self.gpio.digitalWrite(self.vprg, self.HIGH)
        self.gpio.digitalWrite(self.vprg, self.HIGH)
        os.write(self.spi_fd, dc_buffer)

    def write_pwm(self, pwm_values):
        """ Write the PWM output levels.

            :param numpy.array pwm_values:
                A numpy array with the PWM values for each TLC output.
                Each value must be in the range 0-4095 (inclusive).

            Values are written to the TLCs in reverse order (since each value
            is clocked through to the next input).
        """
        pwm_buffer = pack_to_12bit(pwm_values[::-1])
        pwm_buffer = np.bitwise_not(pwm_buffer)
        self.gpio.digitalWrite(self.blank, self.LOW)
        os.write(self.spi_fd, pwm_buffer)
        self.gpio.digitalWrite(self.blank, self.HIGH)
        self.gpio.digitalWrite(self.xlat, self.HIGH)
        self.gpio.digitalWrite(self.xlat, self.LOW)


class Tester:
    """ TLC pin tester. """

    def __init__(self, gsclk, blank, vprg, xlat, dcprg, sin, sclk):
        self.gsclk = gsclk
        self.blank = blank
        self.vprg = vprg
        self.xlat = xlat
        self.dcprg = dcprg
        self.sin = sin
        self.sclk = sclk

        # setup GPIO pins
        self.gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
        self.gpio.pinMode(self.blank, self.gpio.OUTPUT)
        self.gpio.pinMode(self.vprg, self.gpio.OUTPUT)
        self.gpio.pinMode(self.xlat, self.gpio.OUTPUT)
        self.gpio.pinMode(self.dcprg, self.gpio.OUTPUT)

        self.gpio.pinMode(self.gsclk, self.gpio.OUTPUT)
        self.gpio.pinMode(self.sin, self.gpio.OUTPUT)
        self.gpio.pinMode(self.sclk, self.gpio.OUTPUT)

    def test_pins(self):
        """ Test GPIO pins by cycling them each in turn """
        click.echo("Testing IO pins ...")
        for pin_name in [
                'dcprg', 'xlat', 'sin', 'gsclk', 'sclk', 'blank', 'vprg']:
            for state_name in ['high', 'low']:
                pin = getattr(self, pin_name)
                state = getattr(self.gpio, state_name.upper())
                self.gpio.digitalWarite(pin, state)
                click.pause("{} ({}) set {} ...".format(
                    pin_name, pin, state_name))
        click.echo("Test complete.")


@click.command(context_settings={"auto_envvar_prefix": "TSC"})
@click.option(
    '--fps', default=10,
    help='Frames per second.')
@click.option(
    '--frame-addr', default='tcp://127.0.0.1:5556',
    help='ZeroMQ address to publish frames too.')
@click.option(
    '--test-io', default=False, type=bool,
    help='Test IO pins')
def main(fps, frame_addr, test_io):
    click.echo("Tesseract spidev LED driver running.")
    context = zmq.Context()
    frame_socket = context.socket(zmq.SUB)
    frame_socket.connect(frame_addr)
    frame_socket.setsockopt_string(zmq.SUBSCRIBE, u"")  # receive everything

    if test_io:
        tester = Tester(
            gsclk=14, blank=3, vprg=5, xlat=6, dcprg=7, sin=12, sclk=14)
        tester.test_pins()
        return

    # 3 906 250  Hz is the maximum SPI bus speed at which we can
    # correctly clock data into the TLC chips. The factor of 4 was
    # emperically determined as a good balance between time spent
    # in Python code and time spent clocking data in the SPI (faster SPI
    # writes gives faster rendering of each layer, but looping through the
    # layers more often means the LEDs appear less bright because they are only
    # lit while the SPI clock is being toggled).
    max_spispeed = 3906250
    spispeed = max_spispeed / 4

    tlcs = TLCs(
        tlcs=5,
        blank=3, vprg=5, xlat=6, dcprg=7,
        spibus=0, spidevice=0, spispeed=spispeed)

    fc = frame_utils.FrameConstants(fps=fps, ttype="tesseract")
    frame = fc.empty_frame()

    pwm_values = np.zeros(tlcs.n_outputs, dtype=np.uint16)
    layers = list(range(fc.layers))
    layer_masks = [np.zeros(16) for _ in range(fc.layers)]
    for l in layers:
        layer_masks[l][l] = 4095

    tlcs.init_tlcs()
    while True:
        try:
            data = frame_socket.recv(flags=zmq.NOBLOCK)
        except zmq.ZMQError as err:
            if not err.errno == zmq.EAGAIN:
                raise
        else:
            frame = np.frombuffer(data, dtype=frame_utils.FRAME_DTYPE)
            frame.shape = frame_utils.FRAME_SHAPE
        for layer in layers:
            pwm_values[0:16] = layer_masks[layer].ravel()
            # Currently we set LEDs either completely off (intensity <= 125)
            # or completely on (intensity > 125) because this renders without
            # glitches on the mini cube.
            pwm_values[16:] = (frame[layer].ravel() > 125)
            pwm_values[16:] *= 4095
            # These two lines scale the intensity from 0-255 to 0-4095 but
            # are commented out for now because they cause rendering glitches
            # on the mini cube:
            # pwm_values[16:] = frame[layer].ravel()
            # pwm_values[16:] *= 16  # 16 == 4096 / 256
            tlcs.write_pwm(pwm_values)

    click.echo("Tesseract spidev LED driver exited.")
