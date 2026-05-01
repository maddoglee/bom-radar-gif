# bom-radar-gif
Python code to pull data from the Australian BOM (Bureau of Meteorology) and create an animated gif on a Raspberry Pi Zero. This is then used for display on an iPad2 using HA Dashboard. This is the only way I could get the BOM radar working well on the iPad2 along with Home Assistant data.
I was inspired and used code from this really helpful site! https://medium.com/@rolanditaru/create-an-animated-gif-of-the-weather-radar-in-australia-37446a0f4de0

## **Installation**

bomradargif_FTP.py

This file will grab the images from the BOM. Start off with this one to get it working. 
- Make sure python3 is working on your pi. You also have to install PIL or Pillow. Try this ```pip3 install Pillow```
- clone the git repository ```git clone https://github.com/maddoglee/bom-radar-gif```
- edit bomradargif.py for the desired location (in my case it was IDR034, IDR713 is Sydney)
use the BOM website to find the IDR number for the radar you're interested in. Mine is http://www.bom.gov.au/products/IDR034.loop.shtml#skip
- Choose the layers you want to add (eg. background, roads, locations, waterways). The order of the layers is from bottom to top. Take a look at the FTP site to see what options you have for your radar location based on the png files available.
- ```'/var/www/html/radar_images/radar.gif'``` is where the gif goes. Change to wherever you want the gif to go.
- Check the libraries.
- run it with ```python3 bomradargif_FTP.py```
- add it to your crontab. This example makes a gif every 4 mins and outputs errors to a logfile (its in the tmp folder so it gets deleted on every pi reboot) ```*/4 * * * * /usr/bin/python3 /usr/local/bin/bomradar_FTP.py >> /tmp/out.txt 2>&1```

bomradargif_STATIC.py

This file will only grab the radar images and append them to your own map background (e.g Google maps) and custom locations.

- edit bomradargif_STATIC.py to set where your files are. Take a look at the examples of png files I have made for these. I think it looks better than the BOM backgrounds.
- add it to your crontab. This example makes a gif every 4 mins and outputs errors to a logfile (its in the tmp folder so it gets deleted on every pi reboot) ```*/4 * * * * /home/pi/bom-radar-gif/bomradargif.sh >> /tmp/out.txt 2>&1```

## HA Dashboard (Home Assistant)
Here is the widget code I used on Home Assistant to display on the iPad. 
192.168.1.21 is the address of my pi.

```weather_frame:
    widget_type: iframe
    refresh: 60
    frame_style: ""
    img_list:
      - http://192.168.1.21/radar_images/radar.gif
```

## Making it portable

This project now supports configuration through environment variables, which makes it easier to run on Ubuntu or inside Docker.

### Recommended setup

1. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
2. Set paths and run the static script:
   ```bash
   export RADAR_FILES_DIR=/home/pi/bom-radar-gif/bomradarfiles
   export RADAR_OUTPUT_GIF=/var/www/html/radar_images/radar.gif
   python3 bomradargif_STATIC.py
   ```

### Available environment variables

- `RADAR_FILES_DIR` — folder that contains `IDR034.Background1.png` and `IDR034.locations1.png`
- `RADAR_OUTPUT_GIF` — target GIF path
- `RADAR_BACKGROUND_IMAGE` — explicit background image path
- `RADAR_LOCATIONS_IMAGE` — explicit locations overlay path
- `RADAR_FTP_HOST` — BOM FTP server hostname
- `RADAR_FTP_TRANSPARENCIES_DIR` — FTP transparencies directory
- `RADAR_FTP_RADAR_DIR` — FTP radar images directory
- `RADAR_MAX_FRAMES` — number of images to include in the GIF

### Docker

A `Dockerfile` is included for Ubuntu/x86_64 or other Linux hosts.

Build the image:
```bash
docker build -t bom-radar-gif .
```

Run it with mounted folders:
```bash
docker run --rm \
  -v $(pwd)/bomradarfiles:/app/bomradarfiles \
  -v $(pwd)/output:/app/output \
  bom-radar-gif
```

Then serve `/app/output/radar.gif` from your web server or mount it to your host.
