import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from geopy.geocoders import Nominatim
from geopy.point import Point as GeoPoint

# Define the base directory
base_dir = r"Z:\GLO\GIS"

# Set the initial CRS to the Albers CRS string
crs_source = """
PROJCS["NAD_1983_(2011)_Texas_Centric_Mapping_System_Albers",
GEOGCS["GCS_NAD_1983_2011",
DATUM["D_NAD_1983_2011",
SPHEROID["GRS_1980",6378137.0,298.257222101]],
PRIMEM["Greenwich",0.0],
UNIT["Degree",0.0174532925199433]],
PROJECTION["Albers"],
PARAMETER["false_easting",4921250.0],
PARAMETER["false_northing",19685000.0],
PARAMETER["central_meridian",-100.0],
PARAMETER["standard_parallel_1",27.5],
PARAMETER["standard_parallel_2",35.0],
PARAMETER["latitude_of_origin",18.0],
UNIT["Foot_US",0.3048006096012192]]
"""

# Initialize the geolocator
geolocator = Nominatim(user_agent="myGeocoder")

# Loop over all files in the base directory
for filename in os.listdir(base_dir):
    if filename.endswith(".csv"):
        filepath = os.path.join(base_dir, filename)
        df = pd.read_csv(filepath)

        # Make sure the DataFrame has at least 6 columns
        if df.shape[1] < 6:
            print(f"Skipping {filename} as it has fewer than 6 columns")
            continue

        data = {
            'Name': df.iloc[:, 1].tolist(),
            'X': df.iloc[:, 5].tolist(),
            'Y': df.iloc[:, 4].tolist()
        }

        # Create a GeoDataFrame
        gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data['X'], data['Y']))
        gdf.crs = crs_source

        # Reproject to WGS84 (epsg:4326)
        gdf = gdf.to_crs('EPSG:4326')

        results = []

        # The reprojected coordinates can be accessed as follows:
        for i, row in gdf.iterrows():
            point: Point = row.geometry
            geopoint = GeoPoint(point.y, point.x)  # Note the order: (latitude, longitude)
            location_list = geolocator.reverse(geopoint, exactly_one=False)
            address = "Address not found"
            if location_list:
                for location in location_list:
                    if location.address:
                        address = location.address
                        break
            results.append([row.Name, point.x, point.y, address])

        # Create DataFrame and save to CSV
        result_df = pd.DataFrame(results, columns=["Name", "Longitude", "Latitude", "Address"])
        result_df.to_csv(filepath.rsplit('.', 1)[0] + '_address.csv', index=False)

