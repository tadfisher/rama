#!/bin/sh

DPY=:1
WIDTH=1024
HEIGHT=768

echo "Launching Xephyr on display ${DISPLAY}..."

Xephyr -screen ${WIDTH}x${HEIGHT} $DPY &
sleep 2
DISPLAY=$DPY python rama.py