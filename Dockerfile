FROM debian:latest

ARG DEBIAN_FRONTEND="noninteractive"

# Install python and deps for gdal
RUN apt-get update
RUN apt-get install -y python3 python3-pip build-essential gdal-bin python3-gdal python3-click libgdal-dev wget
RUN echo 'PATH="$HOME/.local/bin/:$PATH"' >>~/.bashrc

# Install deps for tippecanoe
RUN apt-get -y install build-essential libsqlite3-dev zlib1g-dev git
RUN git clone https://github.com/mapbox/tippecanoe.git
WORKDIR /tippecanoe

# Build tippecanoe
RUN make \
  && make install

WORKDIR /app
