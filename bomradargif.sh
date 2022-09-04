#!/bin/sh
echo $(date) >> bash_cron_log.txt
/usr/bin/python3 /home/pi/bom-radar-gif/bomradargif_STATIC.py >> bash_cron_log.txt
