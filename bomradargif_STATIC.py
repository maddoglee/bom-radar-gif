#!/usr/bin/env python3

import io
import os
import sys
import ftplib
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


BASE_DIR = Path(os.getenv("RADAR_APP_DIR", Path(__file__).resolve().parent))
RADAR_FILES_DIR = Path(os.getenv("RADAR_FILES_DIR", BASE_DIR / "bomradarfiles"))
OUTPUT_GIF = Path(os.getenv("RADAR_OUTPUT_GIF", "/var/www/html/radar_images/radar.gif"))
FTP_HOST = os.getenv("RADAR_FTP_HOST", "ftp.bom.gov.au")
FTP_TRANSPARENCIES_DIR = os.getenv("RADAR_FTP_TRANSPARENCIES_DIR", "/anon/gen/radar_transparencies/")
FTP_RADAR_DIR = os.getenv("RADAR_FTP_RADAR_DIR", "/anon/gen/radar/")
MAX_FRAMES = int(os.getenv("RADAR_MAX_FRAMES", "5"))


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


def load_error_font(size=24):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        return ImageFont.load_default()


def save_error_gif(text, output_path):
    error_image = Image.new("RGBA", (500, 300), (255, 0, 0, 255))
    draw = ImageDraw.Draw(error_image)
    font = load_error_font(24)
    draw_centered_multiline_text(draw, text, font, (0, 0, 500, 300))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    error_image.convert("RGB").save(output_path, format="GIF")


# Define the product ID for the radar image based on this URL http://www.bom.gov.au/products/IDR034.loop.shtml
product_id = 'IDR034'
# Initialize an empty list to store the images
frames = []

# The layers that we want to retrieve from the FTP server
layers = ['roads']

# Add the locally stored map background (I made my own background image using Google maps. you can modify the code to use the BOM background image if you want)
BACKGROUND_IMAGE = Path(os.getenv("RADAR_BACKGROUND_IMAGE", RADAR_FILES_DIR / f"{product_id}.Background1.png"))
LOCATIONS_IMAGE = Path(os.getenv("RADAR_LOCATIONS_IMAGE", RADAR_FILES_DIR / f"{product_id}.locations1.png"))

try:
    base_image = Image.open(BACKGROUND_IMAGE).convert('RGBA')
except FileNotFoundError as e:
    print(f"Background image not found: {e}")
    save_error_gif(f"Error: Background image not found.\n{e}", OUTPUT_GIF)
    sys.exit(1)

# Connect to the BOM FTP server to grab the layers
ftp = ftplib.FTP(FTP_HOST)
ftp.login()
ftp.cwd(FTP_TRANSPARENCIES_DIR)

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
    ftp.cwd(FTP_RADAR_DIR)
#    print("Successfully changed directory to /anon/gen/radar/")
except ftplib.error_perm as e:
    print(f"Failed to change directory: {e}")
    ftp.quit()
    sys.exit(1)

# List comprehension to filter out the images we need
# Only include files that start with the product ID and end with .png
# Take the most recent images up to the configured maximum
files = [file for file in ftp.nlst() if file.startswith(product_id) and file.endswith('.png')][-MAX_FRAMES:]

if not files:
    print("No radar images found.")
    save_error_gif("No radar images found.\nPlease check the BOM website for maintenance.", OUTPUT_GIF)
    ftp.quit()
    sys.exit(1)

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
        image = Image.open(LOCATIONS_IMAGE).convert('RGBA')
        frame.paste(image, (0, 0), image)
        frames.append(frame)
    except Exception as e:
        print(f"Error processing {file}: {e}")
        pass

# Close the FTP connection
ftp.quit()

if not frames:
    print("No radar images found.")
    save_error_gif("No radar images found.\nPlease check the BOM website for maintenance.", OUTPUT_GIF)
    sys.exit(1)

if frames:
    # Store the result as a GIF file in a web-accessible folder
    OUTPUT_GIF.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(OUTPUT_GIF, format='GIF', save_all=True, append_images=frames[1:] + [frames[-1], frames[-1]], duration=400, loop=0)

# Used for debugging to see how many pics have been appended.
#print(frames)