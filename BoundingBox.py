import rasterio
from shapely.geometry import Polygon
import pyproj
from pyproj import Transformer
import shapely.ops as ops
import json


def get_polygon_coordinates(file):
    with rasterio.open(file) as dataset:
        # Get bounds of the raster file
        bounds = dataset.bounds

        # Create a Polygon from the bounds
        polygon = Polygon([(bounds.left, bounds.bottom),
                           (bounds.left, bounds.top),
                           (bounds.right, bounds.top),
                           (bounds.right, bounds.bottom),
                           (bounds.left, bounds.bottom)])

        # Define a projection transformation object from the CRS of the raster file to WGS84
        transformer = Transformer.from_crs(dataset.crs, "EPSG:4326", always_xy=True)

        # Transform function for shapely
        transform_func = lambda x, y: transformer.transform(x, y)

        # Apply the projection transformation
        polygon_wgs84 = ops.transform(transform_func, polygon)

        # Convert the Polygon into a GeoJSON formatted string
        geojson_polygon = {
            "type": "Polygon",
            "coordinates": [list(polygon_wgs84.exterior.coords)]
        }

        return geojson_polygon


file = 'Terrain.cudem_ft.tif'
geojson_data = get_polygon_coordinates(file)
print(geojson_data)

# Write the GeoJSON data to a file
with open('output.geojson', 'w') as f:
    json.dump(geojson_data, f)
