FROM python:3.9.2-slim-buster
WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
  && apt-get install libgl1 -y \
  && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 \
  && apt-get install wget -y \
  && apt-get install xz-utils -y \
      && wget https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-n6.1-latest-linux64-gpl-6.1.tar.xz && tar -xvf *xz && cp *6.1/bin/* /usr/bin && rm -rf *xz && rm -rf *6.1 \
  && pip3 install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y ffmpeg
COPY . .
CMD ["bash","start.sh"]
