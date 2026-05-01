#!/bin/sh

PROCESS_NAME="${RADAR_PROCESS_NAME:-bomradargif_STATIC.py}"
FILE_PATH="${RADAR_OUTPUT_GIF:-/var/www/html/radar_images/radar.gif}"
PYTHON="${RADAR_PYTHON:-/usr/bin/python3}"
SCRIPT="${RADAR_SCRIPT:-/home/pi/bom-radar-gif/bomradargif_STATIC.py}"
LOG_FILE="${RADAR_LOG_FILE:-/var/log/radar_process.log}"
CHECK_AGE_MINUTES="${RADAR_CHECK_AGE_MINUTES:-10}"

if pgrep -f "$PROCESS_NAME" > /dev/null; then
    echo "The process $PROCESS_NAME is running."

    if [ "$(find "$FILE_PATH" -mmin +$CHECK_AGE_MINUTES)" ]; then
        echo "The file $FILE_PATH is older than $CHECK_AGE_MINUTES minutes."
        echo "$(date): The file $FILE_PATH is older than $CHECK_AGE_MINUTES minutes. Restarting the process." >> "$LOG_FILE"
        pkill -f "$PROCESS_NAME"
        "$PYTHON" "$SCRIPT"
    else
        echo "The file $FILE_PATH is not older than $CHECK_AGE_MINUTES minutes."
    fi
else
    "$PYTHON" "$SCRIPT"
fi
