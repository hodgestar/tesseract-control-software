#!/bin/sh

while true; do
  /home/pi/tesseract-control-software/ve/bin/tesseract-effectbox \
    --fps 10 \
    --transition 30 \
    --etype tesseract \
    >> /home/pi/effectbox.log
done
