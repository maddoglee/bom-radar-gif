#!/bin/bash

# Path to the file
FILE="/var/www/html/radar_images/radar.gif"
# Path to the logfile
LOGFILE="/var/log/check_file.log"

# Get the current time and the file's modification time
CURRENT_TIME=$(date +%s)
FILE_MOD_TIME=$(stat -c %Y "$FILE")

# Calculate the time difference in seconds
TIME_DIFF=$((CURRENT_TIME - FILE_MOD_TIME))

# Check if the file has been modified in the last 10 minutes (600 seconds)
if [ $TIME_DIFF -gt 600 ]; then
  # Get the last reboot time using uptime -s
  LAST_REBOOT=$(uptime -s)
  LAST_REBOOT_TIME=$(date -d "$LAST_REBOOT" +%s)

  # Calculate the time since the last reboot in seconds
  TIME_SINCE_REBOOT=$((CURRENT_TIME - LAST_REBOOT_TIME))

  # Convert the time since the last reboot to a human-readable format
  TIME_SINCE_REBOOT_HUMAN=$(date -d@$TIME_SINCE_REBOOT -u +%H:%M:%S)

  # Log the time since the last reboot and the reboot action
  echo "$(date): Time since last reboot: $TIME_SINCE_REBOOT_HUMAN" >> $LOGFILE
  echo "$(date): File has not been modified in the last 10 minutes. Rebooting..." >> $LOGFILE
  sudo reboot
else
  echo "$(date): File has been modified in the last 10 minutes. No action needed."
fi