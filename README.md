# bom-radar-gif
Python code to pull data from the Australian BOM (Bureau of Meteorology) and create an animated gif on a raspberry pi. This is then used for display on an iPad2 using HA Dashboard. This is the only way I could get the BOM radar working well on the iPad2 along with Home Assistant data.

## **Installation**

- clone the git repository ```git clone https://github.com/maddoglee/bom-radar-gif```
- edit bomradargif.py for the desired location (in my case it was ID034)
use the BOM website to find the IDR number for the radar you're interested in. Mine is http://www.bom.gov.au/products/IDR034.loop.shtml#skip
- Choose the layers you want to add (eg. background, roads, locations, waterways). Take a look at the FTP site to see what options you have for your radar location based on the png files available.
- Copy bomradargif.py and folder bomradarfiles to /usr/local/bin ```sudo cp -r b* /usr/local/bin/```
- 
