# Above-Ground Biomass (AGB) Model Documentation

## Overview
This document describes the implementation of an above-ground biomass (AGB) estimation model based on the publication:

> **"Estimation of above‑ground biomass in tropical afro‑montane forest using Sentinel‑2 derived indices"**  
> *Seid Muhe and Mekuria Argaw (2022), Environmental Monitoring and Assessment*  
> DOI: [10.1007/s40068-022-00250-y](https://doi.org/10.1007/s40068-022-00250-y)  
> [View PDF](../docs/references/2022_Muhe_EstimationAGBTropicalAfroMontane.pdf)

## Script Sequence
1. `3. AGB_Model_Sentinel2_Template.js`: Implements the AGB estimation model using Sentinel-2 data
2. `4. AGB_Model_Comparison_vCCI.js`: Compares the model results with ESA CCI AGB data

## Detailed Process

### 1. AGB Model Computation

#### Input Data
- Sentinel-2 SR Harmonized median composite for 2021

#### Vegetation Indices
- `NDVI` - Normalized Difference Vegetation Index
- `EVI` - Enhanced Vegetation Index
- `IRECI` - Inverted Red-Edge Chlorophyll Index

#### Derived Biophysical Parameters
- `LAI` - Leaf Area Index from EVI
- `FAPAR` - Fraction of Absorbed Photosynthetically Active Radiation from NDVI
- `FCOVER` - Fractional Vegetation Cover from NDVI

#### Model Formula
AGB = (20.176 × B4) + (6.633 × FCOVER) − (6.180 × FAPAR) + (13.452 × LAI) − (6.307 × IRECI) − 2.282

#### Output Scaling
- Converted from tons/pixel to **Mg/ha (tons/hectare)** by applying a scale factor of 25

### 2. Export to Asset
- The modeled 2021 AGB image is exported to: `projects/ee-komba/assets/AGB_2021`
- Resolution: 100 meters (to match CCI data)

### 3. Comparison with CCI Biomass
- **Reference Dataset**: ESA CCI AGB v4.0 for 2021
- **Layer Comparison**:
  - Model AGB vs CCI AGB visualization
  - Difference map (`Model - CCI`) for spatial inspection
- **Statistical Analysis**:
  - 1000 random sample points over the AOI
  - Values extracted from both datasets
  - Scatter plot with trendline and R² for visual correlation
- **Data Export**:
  - All sampled comparison points exported as CSV

## Outputs

### Map Layers
- `CCI AGB 2021 (Mg/ha)`
- `Model AGB 2021 (Mg/ha)`
- `Model - CCI Difference`

### Charts
- Scatter plot of `Model AGB` vs `CCI AGB` with trendline

### File Exports
- CSV file: `AGB_Model_vs_CCI_SamplePoints.csv`

## Important Notes
- The model is sensitive to spectral variation; proper cloud masking and quality filtering is assumed
- The CCI AGB product represents woody vegetation and is derived from radar backscatter
- Validation is most meaningful over forested or vegetated areas, not bare land or croplands 