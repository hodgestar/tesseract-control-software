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
import datetime
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
    b = np.bitwise_not(b)
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
            self, tlcs, gsclk, blank, vprg, xlat, dcprg, sin, sclk,
            spibus=0, spidevice=0, spispeed=500000, inverted=True,
            test=False):
        self.n_tlcs = tlcs
        self.n_outputs = self.n_tlcs * 16  # 16 outputs per TLC
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

        if inverted:
            self.HIGH = self.gpio.LOW
            self.LOW = self.gpio.HIGH
        else:
            self.HIGH = self.gpio.HIGH
            self.LOW = self.gpio.LOW
        # setup SPI
        if not test:
            self.spi = spidev.SpiDev()
            self.spi.open(spibus, spidevice)
            self.spi.max_speed_hz = spispeed
            if inverted:
                self.spi.mode = 0b10  # invert clock signal
        else:
            self.gpio.pinMode(self.gsclk, self.gpio.OUTPUT)
            self.gpio.pinMode(self.sin, self.gpio.OUTPUT)
            self.gpio.pinMode(self.sclk, self.gpio.OUTPUT)

    def init_tlcs(self):
        """ Initialize the TLCs."""
        self.gpio.digitalWrite(self.dcprg, self.LOW)
        self.gpio.digitalWrite(self.vprg, self.HIGH)
        self.gpio.digitalWrite(self.xlat, self.LOW)
        self.gpio.digitalWrite(self.blank, self.HIGH)
        self.gpio.digitalWrite(self.vprg, self.LOW)
        #self.write_dc(np.array([0] * self.n_outputs))
        #raw_input(".write_dc")
        
        self.write_pwm(np.array([4095] * self.n_outputs))
        self.spi.writebytes(np.array([1]).tolist())
        
    def write_dc(self, dc_values):
        """ Write the dot clock (DC) levels.

            :param numpy.array dc_values:
                A numpy array with the dot clock values for each TLC output.
                Each value must be in the range 0-63 (inclusive).

            Values are written to the TLCs in reverse order (since each value
            is clocked through to the next input).
        """
        self.gpio.digitalWrite(self.dcprg, self.HIGH)
        raw_input("self.dcprg, self.HIGH")
        self.gpio.digitalWrite(self.vprg, self.HIGH)
        raw_input("self.vprg, self.HIGH")
        dc_buffer = pack_to_6bit(dc_values[::-1])
        self.gpio.digitalWrite(self.vprg, self.HIGH)
        self.spi.writebytes(dc_buffer.tolist())

    def write_pwm(self, pwm_values):
        """ Write the PWM output levels.

            :param numpy.array pwm_values:
                A numpy array with the PWM values for each TLC output.
                Each value must be in the range 0-4095 (inclusive).

            Values are written to the TLCs in reverse order (since each value
            is clocked through to the next input).
        """
        print(pwm_values.tolist())        
        pwm_buffer = pack_to_12bit(pwm_values[::-1])
        print(pwm_buffer.tolist())        
        self.spi.writebytes(pwm_buffer.tolist())
        self.gpio.digitalWrite(self.blank, self.HIGH)
        self.gpio.digitalWrite(self.xlat, self.HIGH)
        self.gpio.digitalWrite(self.xlat, self.LOW)
        self.gpio.digitalWrite(self.blank, self.LOW)
        
    def test_io(self):
        """ Test GPIO pins by cycling them each in turn """
        click.echo("Test IO.")
        self.gpio.digitalWrite(self.dcprg, self.gpio.HIGH)
        raw_input("dcprg (" + str(self.dcprg) + "), Q1, high...")
        self.gpio.digitalWrite(self.dcprg, self.gpio.LOW)
        raw_input("dcprg (" + str(self.dcprg) + "), Q1, low...")
        self.gpio.digitalWrite(self.xlat, self.gpio.HIGH)
        raw_input("xlat (" + str(self.xlat) + "), Q2, high...")
        self.gpio.digitalWrite(self.xlat, self.gpio.LOW)
        raw_input("xlat (" + str(self.xlat) + "), Q2, low...")
        self.gpio.digitalWrite(self.sin, self.gpio.HIGH)
        raw_input("sin (" + str(self.sin) + "), Q3, high...")
        self.gpio.digitalWrite(self.sin, self.gpio.LOW)
        raw_input("sin (" + str(self.sin) + "), Q3, low...")
        self.gpio.digitalWrite(self.gsclk, self.gpio.HIGH)
        raw_input("gsclk (" + str(self.gsclk) + "), Q4, high...")
        self.gpio.digitalWrite(self.gsclk, self.gpio.LOW)
        raw_input("gsclk (" + str(self.gsclk) + "), Q4, low...")
        self.gpio.digitalWrite(self.sclk, self.gpio.HIGH)
        raw_input("sclk (" + str(self.sclk) + "), Q5, high...")
        self.gpio.digitalWrite(self.sclk, self.gpio.LOW)
        raw_input("sclk (" + str(self.sclk) + "), Q5, low...")
        self.gpio.digitalWrite(self.blank, self.gpio.HIGH)
        raw_input("blank (" + str(self.blank) + "), Q6, high...")
        self.gpio.digitalWrite(self.blank, self.gpio.LOW)
        raw_input("blank (" + str(self.blank) + "), Q6, low...")
        self.gpio.digitalWrite(self.vprg, self.gpio.HIGH)
        raw_input("vprg (" + str(self.vprg) + "), Q7, high...")
        self.gpio.digitalWrite(self.vprg, self.gpio.LOW)
        raw_input("vprg (" + str(self.vprg) + "), Q7, low...")

        click.echo("Test complete.")

    def test_io(self):
        """ Test GPIO pins by cycling them each in turn """
        click.echo("Testing IO pins ...")
        for pin_name in ['vprg', 'gsclk', 'blank', 'xlat']:
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

    tlcs = TLCs(
        tlcs=5, gsclk=14, blank=3, vprg=5, xlat=6, dcprg=7, sin=12, sclk=14,
        spibus=0, spidevice=0, spispeed=500000, test=test_io)
    if test_io:
        tlcs.test_io()
        return

    fc = frame_utils.FrameConstants(fps=fps, ttype="tesseract")
    frame = fc.empty_frame()

    pwm_values = np.zeros(tlcs.n_outputs, dtype=np.uint16)
    layers = list(range(fc.layers))
    layer_masks = [np.zeros(16) for _ in range(fc.layers)]
    for l in layers:
        # for k in range(16):
        #     layer_masks[l][k] = 4095
        # layer_masks[l][l] = 0
        layer_masks[l][l] = 4095
    
    tlcs.init_tlcs()
    zmq_frame = 0
    cycle = 0
    while True:
        try:
            data = frame_socket.recv(flags=zmq.NOBLOCK)
            zmq_frame += 1
        except zmq.ZMQError as err:
            if not err.errno == zmq.EAGAIN:
                raise
        else:
            frame = np.frombuffer(data, dtype=frame_utils.FRAME_DTYPE)
            frame.shape = frame_utils.FRAME_SHAPE
        for layer in layers:
            pwm_values[0:16] = layer_masks[layer].ravel()
            #pwm_values[16:32] = layer_masks[layer].ravel()
            #pwm_values[32:48] = layer_masks[layer].ravel()
            #pwm_values[48:64] = layer_masks[layer].ravel()
            #pwm_values[64:] = layer_masks[layer].ravel()
            pwm_values[16:96] = frame[layer].ravel() * 16  # 16 == 4096 / 256
            tlcs.write_pwm(pwm_values)
        cycle += 1
        if (cycle % 100) == 0:
            print(zmq_frame, cycle, datetime.datetime.now().time())
        

    click.echo("Tesseract spidev LED driver exited.")
