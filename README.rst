Tesseract Control Software
==========================

Version 2 of the control software for the Tesseract.

The Tesseract is an 8 x 8 x 8 monochrome array of LEDs controlled by
an set of TLC LED driver chips.

It comes in two parts in Python:

* ``tesseract-effectbox``: The numpy-based Python application that generates
  effect events and sends frames to display on the Tesseract.

* ``tesseract-simulator``: The Python application that displays frames if
  you don't have real Tesseract hardware to display them on.

And one part in C:

* A hardware driver that displays frames on the real Tesseract hardware.

The pieces communicate using ZeroMQ.

Version 1 of the software is available at https://github.com/decoydavid/tesseract/
and was written entirely in C with an abandoned implementation in Python.


Todo
----

* Uninvert layers.
* Fix missing corner in cube sprite.
* Add f(xy, t) -> z sprite.
* Add a few animations using f(xy, t) -> t.
* Add rain animation.
* Shuffling blocks animation.
* Slow down all / some animations.
* Never repeat the same animation straight after itself.


Implemented ideas
-----------------

* Initial effectbox implementation.
* Simple effect for testing.
* Initial simulator.
* Cube sprite.
* Sphere sprite.
* Text animation.


Discarded ideas
---------------

* Nothing yet.


Effect ideas
------------

* Nothing yet.


Calibration
-----------

* No implemented yet.


Quickstart
----------

Install the Tesseract control software::

    $ pip install tessled[simulator]  # not yet available

Or::

    $ pip install -e .[simulator]  # for development

Or::

    $ pip install -e .[spidev]  # for driving the LEDs on the Raspberry Pi

Run the API, EffectBox and simulator::

    $ tesseract-effectbox
    $ tesseract-simulator

Or run everything together at once::

    $ tesseract-runner

Or run the SPI LED driver on the Pi::

    $ tesseract-spidev-driver
