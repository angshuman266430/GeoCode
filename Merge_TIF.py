import rasterio
from rasterio.merge import merge
from rasterio.plot import show
import glob
import os

# File paths
dirpath = "Z:\\GIS\\comparetif\\"
out_fp = os.path.join(dirpath, "MergedRaster.tif")

# Make a search criteria to select the .tif files in the directory
search_criteria = "CompareWSE_OPT-Base_DataOnly_Isaac.Terrain.*.tif"
q = os.path.join(dirpath, search_criteria)

# Glob the filenames that match the criteria
tif_fps = glob.glob(q)

# Create an empty list for the datafiles that will be appended into this list
src_files_to_mosaic = []

# Open raster files and append them to the list
for fp in tif_fps:
    src = rasterio.open(fp)
    src_files_to_mosaic.append(src)

# Merge function returns a single mosaic array and the transformation info
mosaic, out_trans = merge(src_files_to_mosaic)

# Copy the metadata from the first raster file in the list
out_meta = src_files_to_mosaic[0].meta.copy()

# Update the metadata to use the merged transform and height/width
out_meta.update({
    "driver": "GTiff",
    "height": mosaic.shape[1],
    "width": mosaic.shape[2],
    "transform": out_trans,
})

# Write the mosaic raster to disk
with rasterio.open(out_fp, "w", **out_meta) as dest:
    dest.write(mosaic)

print("Merged raster created at: ", out_fp)
