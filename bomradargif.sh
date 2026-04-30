#!/bin/sh

# Define the process name to check
process_name="bomradargif_STATIC.py"
# Define the file to check
file_path="/var/www/html/radar_images/radar.gif"
# Define the log file
log_file="/var/log/radar_process.log"

# Check if the process is running
if pgrep -f "$process_name" > /dev/null; then
    echo "The process $process_name is running."
    
    # Check if the file is older than 10 minutes
    if [ $(find "$file_path" -mmin +10) ]; then
        echo "The file $file_path is older than 10 minutes."
        
        # Log the event
        echo "$(date): The file $file_path is older than 10 minutes. Restarting the process." >> "$log_file"
        
        # Kill the process
        pkill -f "$process_name"
        
        # Restart the process
        /usr/bin/python3 /home/pi/bom-radar-gif/bomradargif_STATIC.py
    else
        echo "The file $file_path is not older than 10 minutes."
    fi
else
    # Start the process if it's not running
    /usr/bin/python3 /home/pi/bom-radar-gif/bomradargif_STATIC.py
fi
