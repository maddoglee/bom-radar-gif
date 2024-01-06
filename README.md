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
