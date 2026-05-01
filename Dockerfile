FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV RADAR_FILES_DIR=/app/bomradarfiles
ENV RADAR_OUTPUT_GIF=/app/output/radar.gif
ENV RADAR_FTP_HOST=ftp.bom.gov.au
ENV RADAR_FTP_TRANSPARENCIES_DIR=/anon/gen/radar_transparencies/
ENV RADAR_FTP_RADAR_DIR=/anon/gen/radar/

VOLUME ["/app/bomradarfiles", "/app/output"]

CMD ["python", "bomradargif_STATIC.py"]
