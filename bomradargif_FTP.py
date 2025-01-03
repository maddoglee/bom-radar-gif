#!/usr/bin/env python3

# Removed this line since updating my pi to use python 3.9.18. It shouldn't be needed if you have your python env set up correctly.
#import sys 
#sys.path = ['/usr/lib/python37.zip', '/usr/lib/python3.7', '/usr/lib/python3.7/lib-dynload', '/home/pi/.local/lib/python3.7/site-packages', '/usr/local/lib/python3.7/dist-packages', '/usr/lib/python3/dist-packages']

import io
import ftplib
from PIL import Image

product_id = 'IDR034' # The ID for our radar image - IDR713 = Sydney
frames = [] # List to store the images

# The layers that we want in the order from bottom to top
layers = ['background', 'topography', 'roads', 'waterways', 'catchments', 'locations']

# Add the locally stored map background
#filename = f"/usr/local/bin/bomradarfiles/{product_id}.Background1.png"
#base_image = Image.open(filename).convert('RGBA')

# connect to the BOM ftp server to grab the layers
ftp = ftplib.FTP('ftp.bom.gov.au')
ftp.login()
ftp.cwd('anon/gen/radar_transparencies/')

for layer in layers:
 filename = f"{product_id}.{layer}.png"
 file_obj = io.BytesIO()
 ftp.retrbinary('RETR ' + filename, file_obj.write)
 if layer == 'background':
  base_image = Image.open(file_obj).convert('RGBA')
 else:
  image = Image.open(file_obj).convert('RGBA')
  base_image.paste(image, (0,0), image)

# Access the FTP server to get the radar images
ftp = ftplib.FTP('ftp.bom.gov.au')
ftp.login()
ftp.cwd('anon/gen/radar/')

# List comprehension to filter out the images we need
# Make sure the filename starts with the radar ID, and it ends with .png
# Take the last 5 images, since it is the most recent ones
files = [file for file in ftp.nlst() \
 if file.startswith(product_id) \
 and file.endswith('.png')][-5:]

# Loop over the files and append the image data into our image list
for file in files:
 file_obj = io.BytesIO()
 try:
  ftp = ftplib.FTP('ftp.bom.gov.au')
  ftp.login()
  ftp.cwd('anon/gen/radar/')
  ftp.retrbinary('RETR ' + file, file_obj.write)
  image = Image.open(file_obj).convert('RGBA')
  frame = base_image.copy()
  frame.paste(image, (0,0),image)
  frames.append(frame)

# get locations from BOM FTP. Paste location pic on top of radar images (so the radar doesn't cover the location names)
# you can comment out this code if you prefer the radar
  ftp = ftplib.FTP('ftp.bom.gov.au')
  ftp.login()
  ftp.cwd('anon/gen/radar_transparencies/')
  filename = f"{product_id}.locations.png"
  file_obj = io.BytesIO()
  ftp.retrbinary('RETR ' + filename, file_obj.write)
  image = Image.open(file_obj).convert('RGBA')

# use local stored image for locations (must be transparent). This will paste locations on top of radar images
#  filename = f"/usr/local/bin/bomradarfiles/{product_id}.locations1.png"
#  image = Image.open(filename).convert('RGBA')

# paste either FTP or local locations
  frame.paste(image, (0,0), image)
  frames.append(frame)
 except ftplib.all_errors:
  pass

ftp.quit()

# Store the result as a GIF file in web accessible folder
frames[0].save('/var/www/html/radar_images/radar.gif', format='GIF', save_all=True, append_images=frames[1:]+[frames[-1],frames[-1]], duration=400, loop=0)
#used for debugging to see how many pics have been appended.
print(frames)
