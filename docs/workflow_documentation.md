# Workflow Documentation

## Overview
This document describes the workflow for processing temporal land cover data using Google Earth Engine (GEE) and Python scripts. The workflow is designed to process and analyze land cover changes over time, with a focus on NDVI (Normalized Difference Vegetation Index) analysis and land cover classification.

## Script Workflow

### 1. Google Earth Engine Scripts

#### 1.1 Landsat_NDVI_SpecificYears.js
- Purpose: Extracts NDVI values from Landsat imagery for specific years
- Input: Landsat imagery collection
- Processing:
  - Calculates NDVI for selected years
  - Applies cloud masking
  - Performs temporal analysis
- Output: NDVI time series data

#### 1.2 ndvi_landcover_masking_export.js
- Purpose: Applies land cover masking to NDVI data
- Input: NDVI time series from previous step
- Processing:
  - Applies land cover classification masks
  - Filters for specific land cover types
  - Exports masked data
- Output: Masked NDVI data ready for vectorization

### 2. Python Processing Scripts

#### 2.1 raster_to_vector_with_csv.ipynb
- Purpose: Converts raster data to vector format with associated CSV data
- Input: Raster data from GEE exports
- Processing:
  - Raster to vector conversion
  - Attribute extraction
  - CSV data generation
- Output: Vector files and associated CSV data

#### 2.2 merge_csv.ipynb
- Purpose: Merges multiple CSV files containing temporal data
- Input: Multiple CSV files with temporal information
- Processing:
  - Data alignment
  - Temporal merging
  - Data validation
- Output: Combined CSV with merged temporal data

#### 2.3 stratified_biomass_sampler.ipynb
- Purpose: Performs stratified sampling for biomass analysis
- Input: Vector data and biomass information
- Processing:
  - Stratification
  - Sample selection
  - Statistical analysis
- Output: Sampled points and analysis results

#### 2.4 extract_polygons.ipynb
- Purpose: Extracts polygons based on specific criteria
- Input: Vector data and selection criteria
- Processing:
  - Polygon extraction
  - Attribute filtering
  - Spatial analysis
- Output: Selected polygons meeting criteria

#### 2.5 combine_vectors.ipynb
- Purpose: Combines multiple vector files
- Input: Multiple vector files
- Processing:
  - Vector merging
  - Attribute handling
  - Spatial operations
- Output: Combined vector file

#### 2.6 combine_area_polygons_by_coords.py
- Purpose: Combines area polygons based on coordinates
- Input: Polygon data and coordinate information
- Processing:
  - Coordinate-based merging
  - Area calculations
  - Spatial aggregation
- Output: Combined area polygons

## Data Flow
1. Data Collection
   - Landsat imagery via GEE
   - NDVI calculation and masking
   - Export to raster format

2. Data Processing
   - Raster to vector conversion
   - Temporal data merging
   - Spatial analysis

3. Output Generation
   - Vector files
   - CSV data
   - Analysis results

## Dependencies
- Google Earth Engine
- Python 3.x
- Required Python packages:
  - pandas
  - geopandas
  - numpy
  - rasterio
  - shapely

## Usage Notes
- Ensure GEE authentication is set up before running GEE scripts
- Python scripts can be run in sequence or independently based on needs
- All scripts include error handling and logging
- Output files follow a consistent naming convention
