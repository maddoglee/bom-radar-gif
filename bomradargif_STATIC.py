#!/usr/bin/env python3

import io
import ftplib
import textwrap
from PIL import Image, ImageDraw, ImageFont


def draw_centered_multiline_text(draw, text, font, box, fill=(255, 255, 255, 255), line_spacing=6):
    lines = []
    for paragraph in text.split("\n"):
        wrapped = textwrap.wrap(paragraph, width=28)
        if not wrapped:
            wrapped = [""]
        lines.extend(wrapped)

    line_sizes = [draw.textbbox((0, 0), line, font=font) for line in lines]
    line_heights = [bbox[3] - bbox[1] for bbox in line_sizes]
    total_height = sum(line_heights) + line_spacing * (len(lines) - 1)

    y = box[1] + ((box[3] - box[1]) - total_height) // 2
    for line, bbox, height in zip(lines, line_sizes, line_heights):
        line_width = bbox[2] - bbox[0]
        x = box[0] + ((box[2] - box[0]) - line_width) // 2
        draw.text((x, y), line, fill=fill, font=font)
        y += height + line_spacing


# Define the product ID for the radar image based on this URL http://www.bom.gov.au/products/IDR034.loop.shtml
product_id = 'IDR034'
# Initialize an empty list to store the images
frames = []

# The layers that we want to retrieve from the FTP server
layers = ['roads']

# Add the locally stored map background (I made my own background image using Google maps. you can modify the code to use the BOM background image if you want)
filename = f"/home/pi/bom-radar-gif/bomradarfiles/{product_id}.Background1.png"
try:
    base_image = Image.open(filename).convert('RGBA')
except FileNotFoundError as e:
    print(f"Background image not found: {e}")
    # Create an error image
    error_image = Image.new('RGBA', (500, 300), (255, 0, 0, 255))
    draw = ImageDraw.Draw(error_image)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    text = f"Error: Background image not found.\n{e}"
    draw_centered_multiline_text(draw, text, font, (0, 0, 500, 300))
    
    # Convert to RGB for GIF compatibility
    error_image = error_image.convert('RGB')
    
    # Save the error image as a GIF
    error_image.save('/var/www/html/radar_images/radar.gif', format='GIF')
    exit(1)

# Connect to the BOM FTP server to grab the layers
ftp = ftplib.FTP('ftp.bom.gov.au')
ftp.login()
ftp.cwd('/anon/gen/radar_transparencies/')

# List files in the directory
files = ftp.nlst()

# Loop through each layer and retrieve the corresponding file from the FTP server
for layer in layers:
    filename = f"{product_id}.{layer}.png"
    if filename in files:
        # Create an in-memory bytes buffer to store the file data
        file_obj = io.BytesIO()
        # Retrieve the file from the FTP server and write it to the buffer
        ftp.retrbinary('RETR ' + filename, file_obj.write)
        if layer == 'background':
            # If the layer is 'background', open the image and convert it to RGBA
            base_image = Image.open(file_obj).convert('RGBA')
        else:
            # For other layers, open the image and paste it onto the base image
            image = Image.open(file_obj).convert('RGBA')
            base_image.paste(image, (0, 0), image)
    else:
        print(f"File {filename} not found on the server. Skipping...")

# Access the FTP server to get the radar images
try:
 #   print("Changing directory to /anon/gen/radar/")
    ftp.cwd('/anon/gen/radar/')
#    print("Successfully changed directory to /anon/gen/radar/")
except ftplib.error_perm as e:
    print(f"Failed to change directory: {e}")
    ftp.quit()
    exit(1)

# List comprehension to filter out the images we need
# Only include files that start with the product ID and end with .png
# Take the last 5 images, which are the most recent ones
files = [file for file in ftp.nlst() if file.startswith(product_id) and file.endswith('.png')][-5:]

if not files:
    print("No radar images found.")
    
    # Create an error image
    error_image = Image.new('RGBA', (500, 300), (255, 0, 0, 255))
    draw = ImageDraw.Draw(error_image)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    text = "No radar images found.\nPlease check the BOM website for maintenance."
    draw_centered_multiline_text(draw, text, font, (0, 0, 500, 300))
    
    # Convert to RGB for GIF compatibility
    error_image = error_image.convert('RGB')
    
    # Save the error image as a GIF
    error_image.save('/var/www/html/radar_images/radar.gif', format='GIF')
    
    ftp.quit()
    exit(1)

# Loop over the files and append the image data into our image list
for file in files:
    file_obj = io.BytesIO()
    try:
        # Retrieve the radar image from the FTP server and write it to the buffer
        ftp.retrbinary('RETR ' + file, file_obj.write)
        # Open the image and convert it to RGBA
        image = Image.open(file_obj).convert('RGBA')
        # Create a copy of the base image
        frame = base_image.copy()
        # Paste the radar image onto the base image
        frame.paste(image, (0, 0), image)
        # Append the combined image to the frames list
        frames.append(frame)

        # Use local stored image for locations (must be transparent)
        # This will paste locations on top of radar images
        filename = f"/home/pi/bom-radar-gif/bomradarfiles/{product_id}.locations1.png"
        image = Image.open(filename).convert('RGBA')
        frame.paste(image, (0, 0), image)
        frames.append(frame)
    except Exception as e:
        print(f"Error processing {file}: {e}")
        pass

# Close the FTP connection
ftp.quit()

if not frames:
    print("No radar images found.")
    
    # Create an error image
    error_image = Image.new('RGBA', (500, 300), (255, 0, 0, 255))
    draw = ImageDraw.Draw(error_image)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    except OSError:
        font = ImageFont.load_default()
    text = "No radar images found.\nPlease check the BOM website for maintenance."
    draw_centered_multiline_text(draw, text, font, (0, 0, 500, 300))
    
    # Convert to RGB for GIF compatibility
    error_image = error_image.convert('RGB')
    
    # Save the error image as a GIF
    error_image.save('/var/www/html/radar_images/radar.gif', format='GIF')
    
    exit(1)

if frames:
    # Store the result as a GIF file in a web-accessible folder
    frames[0].save('/var/www/html/radar_images/radar.gif', format='GIF', save_all=True, append_images=frames[1:] + [frames[-1], frames[-1]], duration=400, loop=0)

# Used for debugging to see how many pics have been appended.
#print(frames)