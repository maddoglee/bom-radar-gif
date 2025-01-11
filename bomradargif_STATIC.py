#!/usr/bin/env python3

import io
import ftplib
from PIL import Image

product_id = 'IDR034'  # The ID for our radar image.
frames = []  # List to store the images

# The layers that we want
layers = ['roads']

# Add the locally stored map background
filename = f"/home/pi/bom-radar-gif/bomradarfiles/{product_id}.Background1.png"
base_image = Image.open(filename).convert('RGBA')

# Connect to the BOM FTP server to grab the layers
ftp = ftplib.FTP('ftp.bom.gov.au')
ftp.login()
ftp.cwd('/anon/gen/radar_transparencies/')

# List files in the directory
files = ftp.nlst()

for layer in layers:
    filename = f"{product_id}.{layer}.png"
    if filename in files:
        file_obj = io.BytesIO()
        ftp.retrbinary('RETR ' + filename, file_obj.write)
        if layer == 'background':
            base_image = Image.open(file_obj).convert('RGBA')
        else:
            image = Image.open(file_obj).convert('RGBA')
            base_image.paste(image, (0, 0), image)
    else:
        print(f"File {filename} not found on the server. Skipping...")

# Access the FTP server to get the radar images
try:
    print("Changing directory to anon/gen/radar/")
    ftp.cwd('/anon/gen/radar/')
    print("Successfully changed directory to anon/gen/radar/")
except ftplib.error_perm as e:
    print(f"Failed to change directory: {e}")
    ftp.quit()
    exit(1)

# List comprehension to filter out the images we need
files = [file for file in ftp.nlst() if file.startswith(product_id) and file.endswith('.png')][-5:]

# Loop over the files and append the image data into our image list
for file in files:
    file_obj = io.BytesIO()
    try:
        ftp.retrbinary('RETR ' + file, file_obj.write)
        image = Image.open(file_obj).convert('RGBA')
        frame = base_image.copy()
        frame.paste(image, (0, 0), image)
        frames.append(frame)

        # Use local stored image for locations (must be transparent). This will paste locations on top of radar images
        filename = f"/home/pi/bom-radar-gif/bomradarfiles/{product_id}.locations1.png"
        image = Image.open(filename).convert('RGBA')
        frame.paste(image, (0, 0), image)
        frames.append(frame)
    except ftplib.all_errors:
        pass

ftp.quit()

# Store the result as a GIF file in a web-accessible folder
frames[0].save('/var/www/html/radar_images/radar.gif', format='GIF', save_all=True, append_images=frames[1:] + [frames[-1], frames[-1]], duration=400, loop=0)

# Used for debugging to see how many pics have been appended.
#print(frames)