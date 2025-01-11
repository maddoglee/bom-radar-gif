#!/bin/sh

process_name="python3"

if pgrep -x "$process_name" > /dev/null; then
    echo "The process $process_name is running."
else
    echo "The process $process_name is not running."
   /usr/bin/python3 /home/pi/bom-radar-gif/bomradargif_STATIC.py
fi
