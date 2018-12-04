#!/bin/sh

while true; do
  /home/pi/tesseract-control-software/ve/bin/tesseract-spidev-driver \
    --fps 10 \
    >> /home/pi/spidev-driver.log
done
