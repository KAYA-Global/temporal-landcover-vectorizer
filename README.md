# Temporal Land Cover Vectorizer

## Overview
This repository contains a comprehensive suite of tools for processing and analyzing temporal land cover changes using Google Earth Engine (GEE) and Python. The workflow focuses on NDVI (Normalized Difference Vegetation Index) analysis and land cover classification, providing tools for data processing, analysis, and visualization.

## Repository Structure
```
temporal-landcover-vectorizer/
├── scripts/
│   ├── gee/
│   │   ├── 1. Landsat_NDVI_SpecificYears.js
│   │   ├── 2. ndvi_landcover_masking_export.js
│   │   ├── 3. AGB_Model_Sentinel2_Template.js
│   │   └── 4. AGB_Model_Comparison_vCCI.js
│   └── python/
│       ├── 5. raster_to_vector_with_csv.ipynb
│       ├── 6. merge_csv.ipynb
│       ├── 7. stratified_biomass_sampler.ipynb
│       ├── 8. extract_polygons.ipynb
│       ├── 9. combine_vectors.ipynb
│       └── 10. combine_area_polygons_by_coords.py
├── docs/
│   ├── workflow_documentation.md
│   ├── onedrive_setup.md
│   ├── onedrive_readme_template.md
│   └── agb_model_documentation.md
└── README.md
```

## Data Storage
Analysis outputs and large datasets are stored in a dedicated OneDrive folder for better organization and collaboration. The data folder structure is:

```
Temporal Land Cover Analysis/
└── analysis_2024/
    ├── vector_data/      # Vector files (points, polygons)
    ├── csv_data/         # Raw and processed CSV data
    │   ├── raw/          # Original data files
    │   └── processed/    # Processed data files
    └── analysis_results/ # Analysis outputs and reports
```

The OneDrive folder is located at:
```
C:\Users\galag\KAYA Climate Solutions GmbH\Climate - Documents\General\Map projects\Wirong\Temporal Land Cover Analysis
```

For access to the data and detailed folder structure, see `docs/onedrive_setup.md`.

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
git clone https://github.com/KAYA-Global/temporal-landcover-vectorizer.git
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
4. Run `3. AGB_Model_Sentinel2_Template.js` to compute above-ground biomass
5. Run `4. AGB_Model_Comparison_vCCI.js` to compare with ESA CCI data

### 2. Python Processing
1. Run the Python scripts in sequence:
   - `5. raster_to_vector_with_csv.ipynb`: Convert raster data to vector format
   - `6. merge_csv.ipynb`: Merge temporal data
   - `7. stratified_biomass_sampler.ipynb`: Perform biomass sampling
   - `8. extract_polygons.ipynb`: Extract specific polygons
   - `9. combine_vectors.ipynb`: Combine vector files
   - `10. combine_area_polygons_by_coords.py`: Combine area polygons

## Documentation
- `workflow_documentation.md`: Detailed workflow steps and processes
- `onedrive_setup.md`: OneDrive folder structure and setup guide
- `onedrive_readme_template.md`: Template for OneDrive folder documentation
- `agb_model_documentation.md`: Documentation for the AGB estimation model and validation

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details. Copyright © 2024 KAYA-Global.
