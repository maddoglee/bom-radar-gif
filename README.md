# bom-radar-gif
Python code to pull data from the Australian BOM (Bureau of Meteorology) and create an animated gif on a Raspberry Pi Zero. This is then used for display on an iPad2 using HA Dashboard. This is the only way I could get the BOM radar working well on the iPad2 along with Home Assistant data.
I was inspired and used code from this really helpful site! https://medium.com/@rolanditaru/create-an-animated-gif-of-the-weather-radar-in-australia-37446a0f4de0

## Installation & Usage

This project supports multiple deployment methods depending on your platform and preference.

### 1. Raspberry Pi (Python)

For Raspberry Pi users who prefer running Python directly:

```bash
git clone https://github.com/maddoglee/bom-radar-gif.git
cd bom-radar-gif
pip3 install -r requirements.txt
```

Edit environment variables or use defaults:
```bash
export RADAR_FILES_DIR=./bomradarfiles
export RADAR_OUTPUT_GIF=/var/www/html/radar_images/radar.gif
python3 bomradargif_STATIC.py
```

Add to crontab for automated scheduling (every 4 minutes):
```bash
*/4 * * * * cd /home/pi/bom-radar-gif && /usr/bin/python3 bomradargif_STATIC.py >> /tmp/out.txt 2>&1
```

Or use the wrapper script with watchdog logic:
```bash
*/4 * * * * /home/pi/bom-radar-gif/bomradargif.sh >> /tmp/out.txt 2>&1
```

### 2. Ubuntu/Linux (Python)

For running directly on Ubuntu or other Linux systems:

```bash
git clone https://github.com/maddoglee/bom-radar-gif.git
cd bom-radar-gif
pip3 install -r requirements.txt
```

Set your paths:
```bash
export RADAR_FILES_DIR=/path/to/bomradarfiles
export RADAR_OUTPUT_GIF=/var/www/html/radar_images/radar.gif
python3 bomradargif_STATIC.py
```

Create a systemd service or use cron as above.

### 3. Docker Compose (Recommended for Ubuntu/i5 Server)

The easiest way to run on your Ubuntu i5-8600 server:

```bash
git clone https://github.com/maddoglee/bom-radar-gif.git
cd bom-radar-gif
cp .env.example .env
# Edit .env if needed (optional, defaults are usually fine)
docker-compose up -d
```

The container will:
- Run in the background
- Execute the radar GIF generation every 4 minutes
- Mount `./bomradarfiles` for overlay images (read-only)
- Mount `./output` for the generated `radar.gif`
- Restart automatically unless stopped

View logs:
```bash
docker-compose logs -f bom-radar-gif
```

Stop:
```bash
docker-compose down
```

### 4. Docker (Manual)

If you prefer manual Docker without Compose:

```bash
docker build -t bom-radar-gif .
docker run -d \
  --name bom-radar-gif \
  -v $(pwd)/bomradarfiles:/app/bomradarfiles:ro \
  -v $(pwd)/output:/app/output \
  --env-file .env.example \
  --restart unless-stopped \
  bom-radar-gif
```

## Configuration

All paths and FTP settings are configurable via environment variables. See [.env.example](.env.example) for available options:

- `RADAR_FILES_DIR` — folder containing background and overlay images
- `RADAR_OUTPUT_GIF` — where to save the generated GIF
- `RADAR_BACKGROUND_IMAGE` — custom background PNG path
- `RADAR_LOCATIONS_IMAGE` — custom locations overlay PNG path
- `RADAR_FTP_HOST` — BOM FTP server (default: `ftp.bom.gov.au`)
- `RADAR_FTP_TRANSPARENCIES_DIR` — FTP path for layer files
- `RADAR_FTP_RADAR_DIR` — FTP path for radar images
- `RADAR_MAX_FRAMES` — number of images in the GIF (default: 5)

## Creating Custom Background & Overlay Images

You can create your own custom background and locations overlay images:

1. **Background** (`IDR034.Background1.png`):
   - Use Google Maps or your preferred cartography tool
   - Export as PNG with transparency (RGBA)
   - Should be 500x300 pixels for best results

2. **Locations** (`IDR034.locations1.png`):
   - Add points of interest or labels
   - Must have a transparent background (RGBA)
   - Same dimensions: 500x300 pixels

Place these files in the `bomradarfiles/` folder.

## Choosing Your Radar Location

The project defaults to `IDR034` (Brisbane). To use a different location:

1. Find your radar on the [BOM website](http://www.bom.gov.au/products/)
2. Note the IDR number (e.g., `IDR713` for Sydney)
3. Update your background and locations image filenames accordingly
4. Set `RADAR_BACKGROUND_IMAGE` and `RADAR_LOCATIONS_IMAGE` environment variables if using non-standard paths

## Error Display

If the script encounters issues (no radar images, missing files, FTP errors), it will create an error message GIF displayed on your dashboard. This makes it easy to spot problems without checking logs.

## Home Assistant Integration

Display the radar GIF on your Home Assistant dashboard:

```yaml
weather_frame:
  widget_type: iframe
  refresh: 60
  frame_style: ""
  img_list:
    - http://192.168.1.21/radar_images/radar.gif
```

Replace `192.168.1.21` with your Pi or server's IP address, and adjust the path to match your `RADAR_OUTPUT_GIF` setting.

## Release Notes

- **v1.0-rpi**: Stable Raspberry Pi + Python version with error handling (tag: `v1.0-rpi`)
- **main** (latest): Full portability support, Docker/Compose, environment variables
