import geopandas as gpd
from shapely.geometry import Point

# Define the data
data = {
    'Name': ['8761305', '8761927', '8761724', '8764227', '8768094'],
    'Longitude': [-89.67333333, -90.11333333, -89.95666666, -91.33833333, -93.34333333],
    'Latitude': [29.86833333, 30.02666666, 29.26333333, 29.45, 29.76833333]
}

# Create a GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['Longitude'], data['Latitude']))

# Set the initial CRS to WGS84 (epsg:4326)
gdf.crs = 'EPSG:4326'

# Define the target CRS
crs_target = """
PROJCS["USA_Contiguous_Albers_Equal_Area_Conic_USGS_version",
GEOGCS["GCS_North_American_1983",
DATUM["D_North_American_1983",
SPHEROID["GRS_1980",6378137.0,298.257222101]],
PRIMEM["Greenwich",0.0],
UNIT["Degree",0.0174532925199433]],
PROJECTION["Albers"],
PARAMETER["false_easting",0.0],
PARAMETER["false_northing",0.0],
PARAMETER["central_meridian",-96.0],
PARAMETER["standard_parallel_1",29.5],
PARAMETER["standard_parallel_2",45.5],
PARAMETER["latitude_of_origin",23.0],
UNIT["Foot_US",0.3048006096012192]]
"""

# Reproject to the target CRS
gdf = gdf.to_crs(crs_target)

# Save to a shapefile
gdf.to_file("points.shp")
