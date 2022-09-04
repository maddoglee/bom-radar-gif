# bom-radar-gif
Python code to pull data from the Australian BOM (Bureau of Meteorology) and create an animated gif on a raspberry pi. This is then used for display on an iPad2 using HA Dashboard. This is the only way I could get the BOM radar working well on the iPad2 along with Home Assistant data.

## **Installation**

bomradargif_FTP.py

This file will grab the images from the BOM. Start off with this one to get it working. 
- clone the git repository ```git clone https://github.com/maddoglee/bom-radar-gif```
- edit bomradargif.py for the desired location (in my case it was IDR034, IDR713 is Sydney)
use the BOM website to find the IDR number for the radar you're interested in. Mine is http://www.bom.gov.au/products/IDR034.loop.shtml#skip
- Choose the layers you want to add (eg. background, roads, locations, waterways). The order of the layers is from bottom to top. Take a look at the FTP site to see what options you have for your radar location based on the png files available.
- ```'/var/www/html/radar_images/radar.gif'``` is where the gif goes. Change to wherever you want the gif to go.
- run it with ```python3 bomradargif_FTP.py```
- add it to your crontab. This example make a gif every 4 mins. ```*/4 * * * * /usr/bin/python3 /usr/local/bin/bomradar_FTP.py```

bomradargif_STATIC.py

This file will only grab the radar images and append them to your own map background (e.g Google maps) and custom locations.

- edit bomradargif_STATIC.py to
- Copy bomradargif.py and folder bomradarfiles to /usr/local/bin ```sudo cp -r b* /usr/local/bin/```
- 
