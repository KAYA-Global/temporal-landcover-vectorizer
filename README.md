# Temporal Land Cover Vectorizer

## Overview
This repository contains a comprehensive suite of tools for processing and analyzing temporal land cover changes using Google Earth Engine (GEE) and Python. The workflow focuses on NDVI (Normalized Difference Vegetation Index) analysis and land cover classification, providing tools for data processing, analysis, and visualization.

## Repository Structure
```
temporal-landcover-vectorizer/
├── scripts/
│   ├── gee/
│   │   ├── 1. Landsat_NDVI_SpecificYears.js
│   │   └── 2. ndvi_landcover_masking_export.js
│   └── python/
│       ├── 3. raster_to_vector_with_csv.ipynb
│       ├── 4. merge_csv.ipynb
│       ├── 5. stratified_biomass_sampler.ipynb
│       ├── 6. extract_polygons.ipynb
│       ├── 7. combine_vectors.ipynb
│       └── 8. combine_area_polygons_by_coords.py
├── docs/
│   └── workflow_documentation.md
├── data/
│   ├── input/
│   └── output/
├── requirements.txt
└── README.md
```

## Features
- NDVI time series analysis using Landsat imagery
- Land cover classification and masking
- Raster to vector conversion with attribute extraction
- Temporal data merging and analysis
- Stratified sampling for biomass analysis
- Polygon extraction and combination tools
- Coordinate-based area calculations

## Prerequisites
- Google Earth Engine account and authentication
- Python 3.x
- Required Python packages (see requirements.txt):
  - pandas
  - geopandas
  - numpy
  - rasterio
  - shapely

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/temporal-landcover-vectorizer.git
cd temporal-landcover-vectorizer
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up Google Earth Engine authentication:
```bash
earthengine authenticate
```

## Usage

### 1. Google Earth Engine Processing
1. Open the GEE scripts in the Google Earth Engine Code Editor
2. Run `1. Landsat_NDVI_SpecificYears.js` to extract NDVI values
3. Run `2. ndvi_landcover_masking_export.js` to apply land cover masking

### 2. Python Processing
1. Run the Python scripts in sequence:
   - `3. raster_to_vector_with_csv.ipynb`: Convert raster data to vector format
   - `4. merge_csv.ipynb`: Merge temporal data
   - `5. stratified_biomass_sampler.ipynb`: Perform biomass sampling
   - `6. extract_polygons.ipynb`: Extract specific polygons
   - `7. combine_vectors.ipynb`: Combine vector files
   - `8. combine_area_polygons_by_coords.py`: Combine area polygons

## Output
The workflow generates:
- Vector files (points and polygons)
- CSV data with temporal information
- Analysis results and statistics
- Combined area calculations

## Documentation
Detailed workflow documentation is available in `docs/workflow_documentation.md`

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.
