FROM debian:trixie

ARG DEBIAN_FRONTEND="noninteractive"

# Install python and deps for gdal
RUN apt-get update
RUN apt-get install -y python3 python3-pip build-essential gdal-bin python3-gdal python3-click libgdal-dev wget tippecanoe

WORKDIR /project
