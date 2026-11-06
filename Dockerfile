FROM debian:trixie

ARG DEBIAN_FRONTEND="noninteractive"
ARG USERNAME=debian
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
	&& useradd --uid $USER_UID --gid $USER_GID -m $USERNAME

# GDAL (S-57 reading), tippecanoe (tiling), shapely (chart priority clipping),
# Pillow + cairosvg (sprite sheets with light sector icons)
RUN apt-get update && apt-get install -y --no-install-recommends \
	python3 python3-gdal python3-shapely python3-pil python3-cairosvg \
	gdal-bin tippecanoe curl ca-certificates unzip \
	&& rm -rf /var/lib/apt/lists/*

USER $USERNAME

WORKDIR /project
