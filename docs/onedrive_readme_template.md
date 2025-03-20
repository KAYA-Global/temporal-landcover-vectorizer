# Temporal Land Cover Analysis - Wirong Project

## Overview
This folder contains the data and analysis results for the Temporal Land Cover Analysis project for Wirong. The data includes raw inputs, processed data, and final analysis outputs from the temporal-landcover-vectorizer tool.

## Folder Structure
```
analysis_2024/
├── vector_data/
│   └── polygons/
│       └── extracted_polygons.gpkg    # Extracted polygon features
├── csv_data/
│   ├── raw/
│   │   ├── biomass/                   # Raw biomass vectorized data
│   │   │   └── biomass_Area_[5-8]_vectorized.csv
│   │   └── ndfi/                      # Raw NDFI vectorized data
│   │       └── ndfi_Area_[5-8]_vectorized.csv
│   └── processed/
│       └── ndvi/                      # Processed NDVI data
│           └── NDVI_Merged_Area_[5-8].csv
└── analysis_results/
    ├── figures/                       # Analysis visualizations
    ├── reports/                       # Analysis documentation
    └── final_outputs/
        └── sampled_data_with_coords.csv  # Final analysis output
```

## Data Description

### Vector Data
- `extracted_polygons.gpkg`: GeoPackage containing extracted polygon features

### CSV Data
1. Raw Data:
   - Biomass data: Vectorized biomass measurements for areas 5-8
   - NDFI data: Vectorized NDFI (Normalized Difference Fraction Index) for areas 5-8

2. Processed Data:
   - NDVI data: Merged and processed NDVI (Normalized Difference Vegetation Index) for areas 5-8

### Analysis Results
- Final outputs include sampled data with coordinates
- Additional figures and reports will be added as analysis progresses

## Usage Notes
- Data is organized by type and processing stage
- Each dataset corresponds to specific areas (5-8)
- Raw data is preserved separately from processed data
- Final outputs are stored in a dedicated folder

## Related Resources
- Code Repository: https://github.com/yourusername/temporal-landcover-vectorizer
- Documentation: See the repository's docs folder for detailed workflow information

## Contact
For questions about this data or analysis:
- Project Lead: [Name]
- Email: [Email]
- Organization: KAYA Climate Solutions GmbH 