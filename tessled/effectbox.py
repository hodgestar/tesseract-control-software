# -*- coding: utf-8 -*-

""" EffectBox that runs animaitons and publishes frames
    for sending to the Tesseract.

    The EffectBox polls for events regularly, attempting to publish
    frames at regular intervals. Frames are timestamped so that small
    wobbles in processing times can be sorted out in a more realtime
    process (e.g. one written in C or on the Arduino) later.

    If the Tesseract LEDs are viewed as laided in a right-handed coordinate
    system X, Y and Z, where Z is the vertical axis then the frame is a list
    of LEDs with coordinates as follows:

        000, 100, 200, 300, 400, 500, 600, 700
        010, 110, 210, 310, 410, 510, 610, 710
        ...
        001, 101, 201, 301, 401, 501, 601, 701
        011, 111, 211, 311, 411, 511, 611, 711
        ...
        077, 177, 277, 377, 477, 577, 677, 777

    I.e. The rows (constant Y) are laid out one after the other in layers,
    starting with the bottom layer and moving upwards.

    Each monochrome LED is represented by one byte.
"""

import time

import click
import zmq

from .effects.engine import EffectEngine
from .effects.animations import import_animation
from .frame_utils import FrameConstants


@click.command(context_settings={"auto_envvar_prefix": "TSC"})
@click.option(
    '--fps', default=10,
    help='Frames per second.')
@click.option(
    '--ttype', default="tesseract",
    type=click.Choice(FrameConstants.TESSERACT_TYPES.keys()))
@click.option(
    '--transition', default=60,
    help='Time between animation transitions.')
@click.option(
    '--animation', default=None,
    help='Run only a selected set of comma-separated animations.')
@click.option(
    '--frame-addr', default='tcp://127.0.0.1:5556',
    help='ZeroMQ address to publish frames too.')
def main(fps, ttype, transition, animation, frame_addr):
    click.echo("Tesseract effectbox running.")
    tick = 1. / fps
    context = zmq.Context()
    frame_socket = context.socket(zmq.PUB)
    frame_socket.bind(frame_addr)

    fc = FrameConstants(fps=fps, ttype=ttype)
    engine = EffectEngine(fc=fc, tick=tick, transition=transition)
    if animation:
        for name in animation.split(','):
            engine.add_animation_type(import_animation(name))
    else:
        engine.add_default_animation_types()

    while True:
        start = time.time()
        frame = engine.next_frame()
        frame = fc.virtual_to_physical(frame)
        frame_socket.send(frame.tobytes())
        sleep_time = tick - (time.time() - start)
        if sleep_time > 0:
            time.sleep(sleep_time)
    click.echo("Tesseract effectbox exited.")
