# Temporal Land Cover Vectorizer

## Overview
// ... existing code ...

#### B. Vector Conversion
The `raster_timeseries_vectorizer.py` script processes the multi-temporal raster data:
- Input: Multi-band GeoTIFF with temporal bands (2013-2023)
- Processing:
  - Converts masked raster data to vector formats
  - Maintains temporal information
  - Optimizes storage with integer-based values
- Outputs:
  - Point shapefiles (for precise location analysis)
  - Polygon shapefiles (for area analysis)
  - CSV files (for tabular analysis)

#### C. Spatial Data Processing Tools
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ulfboge/temporal-landcover-vectorizer/blob/main/extract_polygons.ipynb)

The repository includes additional tools for processing spatial data:

##### extract_polygons.ipynb
This notebook provides functionality to:
1. Load coordinate points from a CSV file
2. Process multiple shapefiles
3. Extract polygons that intersect with the coordinate points
4. Save results to a GeoPackage file

###### Prerequisites
- pandas
- geopandas
- shapely

These packages will be installed automatically when running the notebook in Google Colab.

###### Input Requirements
1. A CSV file named `sampled_data_with_coords.csv` containing:
   - `x_coord`: X coordinates of the points
   - `y_coord`: Y coordinates of the points
2. A directory named `shapefiles` containing vector layers (*.shp files)

###### Output
The script produces a GeoPackage file (`extracted_polygons.gpkg`) containing all extracted polygons, with each source shapefile saved as a separate layer.

###### Usage
1. Click the "Open in Colab" badge above
2. Upload your input data:
   - The CSV file with coordinates
   - The directory containing your shapefiles
3. Run all cells in sequence

###### Notes
- Uses WGS 84 (EPSG:4326) as default CRS
- Includes optional buffer distance functionality for polygon extraction

### 4. Baseline Assessment Support
// ... rest of existing content ...
