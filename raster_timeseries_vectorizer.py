from osgeo import gdal, ogr, osr
import os
import pandas as pd
import glob

# === Define Base Directories ===
base_directory = r"C:\Users\galag\Wirong\output"

# Subdirectories
raster_folder = os.path.join(base_directory, "raster")
vector_folder = os.path.join(base_directory, "vector")
csv_folder = os.path.join(base_directory, "csv")

# Ensure output subdirectories exist
for folder in [raster_folder, vector_folder, csv_folder]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# === Find All Raster Files Strictly from 'raster' Folder ===
raster_files = []
for file in os.listdir(raster_folder):
    if file.endswith('.tif'):
        full_path = os.path.join(raster_folder, file)
        if os.path.isfile(full_path):
            raster_files.append(full_path)

if not raster_files:
    raise FileNotFoundError(f"No raster files found in '{raster_folder}'.")

# Add debug printing
print("Found the following raster files:")
for file in raster_files:
    print(f"  - {os.path.basename(file)}")

# === Band Names (Fixed for 6 Bands) ===
band_names = ["y2013", "y2015", "y2017", "y2019", "y2021", "y2023"]

# === Process Each Raster ===
for raster_path in raster_files:
    raster_name = os.path.splitext(os.path.basename(raster_path))[0]  # Extract filename without extension
    print(f"\nStarting to process: {raster_name}")

    # Define output file paths
    output_point_shapefile = os.path.join(vector_folder, f"{raster_name}_points.shp")
    output_polygon_shapefile = os.path.join(vector_folder, f"{raster_name}_polygons.shp")
    output_csv_path = os.path.join(csv_folder, f"{raster_name}_vectorized.csv")
    cleaned_csv_path = os.path.join(csv_folder, f"{raster_name}_vectorized_cleaned.csv")

    # Load Raster
    raster_ds = gdal.Open(raster_path)
    if raster_ds is None:
        print(f"Skipping {raster_name}: Could not open raster file.")
        continue

    # Get raster properties
    transform = raster_ds.GetGeoTransform()
    num_bands = raster_ds.RasterCount
    raster_width = raster_ds.RasterXSize
    raster_height = raster_ds.RasterYSize
    origin_x, pixel_width, _, origin_y, _, pixel_height = transform

    # Read raster data into memory
    band_arrays = [raster_ds.GetRasterBand(b).ReadAsArray() for b in range(1, num_bands + 1)]

    # === Create Shapefiles ===
    driver = ogr.GetDriverByName("ESRI Shapefile")
    
    # Create point shapefile
    if os.path.exists(output_point_shapefile):
        driver.DeleteDataSource(output_point_shapefile)
    point_ds = driver.CreateDataSource(output_point_shapefile)

    # Create polygon shapefile
    if os.path.exists(output_polygon_shapefile):
        driver.DeleteDataSource(output_polygon_shapefile)
    polygon_ds = driver.CreateDataSource(output_polygon_shapefile)

    # Set spatial reference (same as raster)
    spatial_ref = osr.SpatialReference()
    spatial_ref.ImportFromWkt(raster_ds.GetProjection())

    # Create layers
    point_layer = point_ds.CreateLayer(f"{raster_name}_points", spatial_ref, ogr.wkbPoint)
    polygon_layer = polygon_ds.CreateLayer(f"{raster_name}_polygons", spatial_ref, ogr.wkbPolygon)

    # Define fields for both layers
    for layer in [point_layer, polygon_layer]:
        layer.CreateField(ogr.FieldDefn("pixel_id", ogr.OFTInteger))
        layer.CreateField(ogr.FieldDefn("x_coord", ogr.OFTReal))
        layer.CreateField(ogr.FieldDefn("y_coord", ogr.OFTReal))

        # Add band fields (limit to max 6 bands) - Changed to Integer type
        actual_band_names = band_names[:num_bands]
        for band_name in actual_band_names:
            layer.CreateField(ogr.FieldDefn(band_name, ogr.OFTInteger))

    # === Process Raster Pixels ===
    csv_data = []
    pixel_id = 1

    for row in range(raster_height):
        for col in range(raster_width):
            x_coord = origin_x + col * pixel_width
            y_coord = origin_y + row * pixel_height

            # Get pixel values
            pixel_values = [band_arrays[b - 1][row, col] for b in range(1, num_bands + 1)]

            # Skip pixels where all bands are 0
            if all(v == 0 for v in pixel_values):
                continue

            # Create point geometry
            point = ogr.Geometry(ogr.wkbPoint)
            point.AddPoint(x_coord, y_coord)

            # Create polygon geometry (pixel boundary)
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(x_coord, y_coord)  # Upper left
            ring.AddPoint(x_coord + pixel_width, y_coord)  # Upper right
            ring.AddPoint(x_coord + pixel_width, y_coord + pixel_height)  # Lower right
            ring.AddPoint(x_coord, y_coord + pixel_height)  # Lower left
            ring.AddPoint(x_coord, y_coord)  # Close the ring
            
            polygon = ogr.Geometry(ogr.wkbPolygon)
            polygon.AddGeometry(ring)

            # Create and set features for both geometries
            for layer, geom in [(point_layer, point), (polygon_layer, polygon)]:
                feature = ogr.Feature(layer.GetLayerDefn())
                feature.SetGeometry(geom)
                feature.SetField("pixel_id", pixel_id)
                feature.SetField("x_coord", x_coord)
                feature.SetField("y_coord", y_coord)
                
                # Set band values - Convert to integer
                for band_idx, band_name in enumerate(actual_band_names):
                    feature.SetField(band_name, int(pixel_values[band_idx]))
                
                layer.CreateFeature(feature)

            # Store data for CSV - Convert band values to integers
            csv_data.append([pixel_id, round(x_coord, 6), round(y_coord, 6)] + [int(v) for v in pixel_values])
            pixel_id += 1

    # Clean up
    point_ds = None
    polygon_ds = None
    raster_ds = None

    # === Export to CSV ===
    csv_columns = ["pixel_id", "x_coord", "y_coord"] + actual_band_names
    df = pd.DataFrame(csv_data, columns=csv_columns)
    df.to_csv(output_csv_path, index=False)
    print(f"CSV saved: {output_csv_path}")

    # === Clean CSV ===
    df[actual_band_names] = df[actual_band_names].applymap(lambda x: int(x) if pd.notnull(x) else "")
    df.to_csv(cleaned_csv_path, index=False)
    print(f"Cleaned CSV saved: {cleaned_csv_path}")

print("Processing complete for all rasters.")