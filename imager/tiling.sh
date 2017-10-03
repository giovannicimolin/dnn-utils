#!/bin/bash

# Generate Tiles
if hash gdal2tiles.py 2>/dev/null; then
	g2t_options="-l -a 0,0,0,0  -p raster -z 0-8 -w none"
	orthophoto_path="media/ortophotos/$1"
	tiles_path="media/ortophoto_tiling/$2/"

	if [ -e "$orthophoto_path" ]; then
		python utils/gdal2tiles-leaflet-master/gdal2tiles-multiprocess.py $g2t_options $orthophoto_path $tiles_path
	else
		echo "No orthophoto found at $orthophoto_path: will skip tiling"
	fi
else
	echo "gdal2tiles.py is not installed, will skip tiling"
fi
