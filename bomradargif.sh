#!/bin/sh
#export PYTHONPATH='/usr/lib/python37.zip' '/usr/lib/python3.7' '/usr/lib/python3.7/lib-dynload', '/home/pi/.local/lib/python3.7/site-packages', '/usr/local/lib/python3.7/dist-packages', '/usr/lib/python3/dist-packages'

process_name="python3"

if pgrep -x "$process_name" > /dev/null; then
    echo "The process $process_name is running."
else
    echo "The process $process_name is not running."
   /usr/bin/python3 /home/pi/bom-radar-gif/bomradargif_STATIC.py
fi
