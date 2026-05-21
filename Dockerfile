FROM debian:trixie

ARG DEBIAN_FRONTEND="noninteractive"
ARG USERNAME=debian
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
	&& useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# Install python and deps for gdal
RUN apt-get update
RUN apt-get install -y python3 python3-pip build-essential gdal-bin python3-gdal python3-click libgdal-dev wget tippecanoe

USER $USERNAME

WORKDIR /project
