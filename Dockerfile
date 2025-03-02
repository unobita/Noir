


# Install ffmpeg (which includes ffprobe)
RUN apt-get update && apt-get install -y ffmpeg
WORKDIR /app
COPY requirements.txt .
RUN apt-get update \
  && apt-get install libgl1 -y \
  && apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 \
  && apt-get install wget -y \
  && apt-get install xz-utils -y \
# Copy your application code


# Install Python dependencies
RUN pip install -r requirements.txt

# Start your application
COPY . .
CMD ["bash","start.sh"]

FROM scalingo/python:latest
