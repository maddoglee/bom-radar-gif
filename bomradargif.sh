#!/bin/sh

process_name="bomradargif_STATIC.py"

if pgrep -f "$process_name" > /dev/null; then
    echo "The process $process_name is running."
else
    echo "The process $process_name is not running."
   /usr/bin/python3 /home/pi/bom-radar-gif/bomradargif_STATIC.py
fi
