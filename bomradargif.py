#!/usr/bin/env python3
import sys
sys.path = ['/usr/lib/python37.zip', '/usr/lib/python3.7', '/usr/lib/python3.7/lib-dynload', '/home/pi/.local/lib/python3.7/site-packages', '/usr/local/lib/python3.7/dist-packages', '/usr/lib/python3/dist-packages']
import io
import ftplib
from PIL import Image

product_id = 'IDR034' # The ID for our radar image
frames = [] # List to store the images

# The layers that we want
#layers = ['background', 'catchments', 'topography', 'roads', 'waterways']
layers = ['roads']

filename = f"/home/pi/bomradar/final/NSWBackground1.png"
#file_obj = io.BytesIO()
#ftp.retrbinary('RETR ' + filename, file_obj.write)
base_image = Image.open(filename).convert('RGBA')

ftp = ftplib.FTP('ftp.bom.gov.au')
ftp.login()
ftp.cwd('anon/gen/radar_transparencies/')

for layer in layers:
 filename = f"{product_id}.{layer}.png"
# print(filename)
 file_obj = io.BytesIO()
 ftp.retrbinary('RETR ' + filename, file_obj.write)
 if layer == 'background':
  base_image = Image.open(file_obj).convert('RGBA')
#  print(base_image)
 else:
  image = Image.open(file_obj).convert('RGBA')
  base_image.paste(image, (0,0), image)

# Access the FTP server
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
#  print(image)
  frame = base_image.copy()
  frame.paste(image, (0,0),image)
  frames.append(frame)
# except ftplib.all_errors:
#  pass

#get locations from FTP paste location pic on top of radar images
#  ftp = ftplib.FTP('ftp.bom.gov.au')
#  ftp.login()
#  ftp.cwd('anon/gen/radar_transparencies/')
#  filename = f"{product_id}.locations.png"
#  file_obj = io.BytesIO()
#  ftp.retrbinary('RETR ' + filename, file_obj.write)
#  image = Image.open(file_obj).convert('RGBA')

# use local image for location

  filename = f"/home/pi/bomradar/final/IDR034.locations1.png"
  image = Image.open(filename).convert('RGBA')
  frame.paste(image, (0,0), image)
  frames.append(frame)
 except ftplib.all_errors:
  pass


ftp.quit()

# Store the result as a GIF file
#frames[0].save('/home/pi/Elements/Projects/radar_images/radar.gif', format='GIF', save_all=True, append_images=frames[1:]+[frames[-1],frames[-1]], duration=400, loop=0)
frames[0].save('/var/www/html/radar_images/radar.gif', format='GIF', save_all=True, append_images=frames[1:]+[frames[-1],frames[-1]], duration=400, loop=0)
print(frames)
#frames[0].save('/var/www/html/radar_images/radar.gif', format='GIF', save_all=True, append_images=frames[:-1], duration=400, loop=0)
