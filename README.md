# MapLibre-Nautical

Convert s57 ENC charts to vector tiles and render them in [MapLibre](https://maplibre.org/) / [Mapbox](https://www.mapbox.com/). MapLibre can be included in various frontends like [Qt](https://github.com/maplibre/maplibre-native-qt), GLFW, iOS, Android, MacOS, Windows and [more](https://github.com/maplibre/awesome-maplibre).

| :exclamation:  The state of the style is early work in progress! |
|-----------------------------------------|

## Worfklow

I am taking [this](https://github.com/Greenroom-Robotics/enc-mapbox-converter) excellent repo to convert to mbtiles and then generate the respective style to render all the information aproppriately. The respective result can be view with [tilserver-gl](https://github.com/maptiler/tileserver-gl) and the style can be improved using [Maputnik](https://maputnik.github.io/), see the following [section](#result).


1. `git clone this repo`
2. `git submodule update --init`
3. `docker compose build`
4. `docker compose run --rm convert_maps`
5. `docker compose run --rm generate_mapstyle`


## Result
- Start tileserver to view vector map with or without style applied:  
    `docker run --rm -v $(pwd)/output:/data -p 8080:8080 maptiler/tileserver-gl`
- Run Maputnik to work on the style:  
    `docker run --rm -it -p 8888:8888 maputnik/editor`  
    To load the generated style and map data, click on `Open`and under `Load from URL` paste this URL: `http://localhost:8080/styles/light/style.json`. 
