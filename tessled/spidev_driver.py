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
        :param int gsclk:
            The (wiringpi) pin number connected to the TLC GSCLK line.
        :param in blank:
            The (wiringpi) pin number connected to the TLC BLANK line.
        :param in vprg:
            The (wiringpi) pin number connected to the TLC VPRG line.
        :param int spibus:
            The number of the SPI bus to use. Default: 0.
        :param int spidevice:
            The number of the SPI device to use. Default: 0.
        :param int spispeed:
            The SPI maximum speed in Hz. Default: 500 kHz.

        Inspired heavily by
        https://github.com/eflukx/enlightenPi/blob/master/TLC5940.py.
    """
    def __init__(
            self, tlcs, gsclk, blank, vprg,
            spibus=0, spidevice=0, spispeed=500000):
        self.n_tlcs = tlcs
        self.n_outputs = self._ntlcs * 16  # 16 outputs per TLC
        self.gsclk = gsclk
        self.blank = blank
        self.vprg = vprg

        # setup SPI
        self.spi = spidev.SpiDev()
        self.spi.open(spibus, spidevice)
        self.spi.max_speed_hz = spispeed

        # setup GPIO pins
        self.gpio = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)
        self.gpio.pinMode(self.gsclkpin, self.gpio.OUTPUT)
        self.gpio.pinMode(self.blankpin, self.gpio.OUTPUT)
        self.gpio.pinMode(self.vprgpin, self.gpio.OUTPUT)

    def init_tlcs(self):
        """ Initialize the TLCs."""
        # stop displaying and reset the internal counter
        self.gpio.digitalWrite(self.blank, self.gpio.HIGH)
        self.gpio.digitalWrite(self.gsclk, self.gpio.LOW)
        # turn LEDs on and disable dot correction (DC)
        self.write_pwm([4095] * self.n_outputs)
        self.write_dc([0] * self.n_outputs)
        # start displaying and start clocking again
        self.gpio.digitalWrite(self.blank, self.gpio.LOW)
        self.gpio.digitalWrite(self.gsclk, self.gpio.HIGH)

    def write_dc(self, dc_values):
        """ Write the dot clock (DC) levels.

            :param numpy.array dc_values:
                A numpy array with the dot clock values for each TLC output.
                Each value must be in the range 0-63 (inclusive).

            Values are written to the TLCs in reverse order (since each value
            is clocked through to the next input).
        """
        dc_buffer = pack_to_6bit(dc_values[::-1])
        self.gpio.digitalWrite(self.vprgpin, self.gpio.HIGH)
        self.spi.writebytes2(dc_buffer)

    def write_pwm(self, pwm_values):
        """ Write the PWM output levels.

            :param numpy.array pwm_values:
                A numpy array with the PWM values for each TLC output.
                Each value must be in the range 0-4095 (inclusive).

            Values are written to the TLCs in reverse order (since each value
            is clocked through to the next input).
        """
        pwm_buffer = pack_to_12bit(pwm_values[::-1])
        self.gpio.digitalWrite(self.vprgpin, self.gpio.LOW)
        self.spi.writebytes2(pwm_buffer)


@click.command(context_settings={"auto_envvar_prefix": "TSC"})
@click.option(
    '--fps', default=10,
    help='Frames per second.')
@click.option(
    '--frame-addr', default='tcp://127.0.0.1:5556',
    help='ZeroMQ address to publish frames too.')
def main(fps, frame_addr):
    click.echo("Tesseract spidev LED driver running.")
    context = zmq.Context()
    frame_socket = context.socket(zmq.SUB)
    frame_socket.connect(frame_addr)
    frame_socket.setsockopt_string(zmq.SUBSCRIBE, u"")  # receive everything

    tlcs = TLCs(
        tlcs=5, gsclk=4, blank=3, vprg=5,
        spibus=0, spidevice=0, spispeed=500000)

    fc = frame_utils.FrameConstants(fps=fps, ttype="tesseract")
    frame = fc.empty_frame()

    pwm_values = np.zeros(tlcs.n_outputs, dtype=np.uint16)
    layers = list(range(fc.layers))
    layer_masks = [np.zeros(16) for _ in range(fc.layers)]
    for l in layers:
        layer_masks[l][l] = 1

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
            pwm_values[0:64] = frame[layer] * 16  # 16 == 4096 / 256
            pwm_values[65:] = layer_masks[layer]
            tlcs.write_pwm(pwm_values)

    click.echo("Tesseract spidev LED driver exited.")
