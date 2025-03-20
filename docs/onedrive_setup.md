# OneDrive Setup and Folder Structure

## Overview
This document provides instructions for setting up and maintaining the OneDrive folder structure for the Temporal Land Cover Vectorizer project. The OneDrive folder serves as the central storage location for all analysis outputs and large datasets.

## OneDrive Folder Structure
```
OneDrive/
└── temporal_landcover_analysis/
    ├── analysis_2024/
    │   ├── vector_data/
    │   │   ├── points/
    │   │   └── polygons/
    │   ├── csv_data/
    │   │   ├── raw/
    │   │   └── processed/
    │   └── analysis_results/
    │       ├── figures/
    │       └── reports/
    ├── previous_analyses/
    │   └── [year]/
    └── README.md
```

## Folder Descriptions

### Main Folders
- `temporal_landcover_analysis/`: Root folder for all project data
- `analysis_2024/`: Current year's analysis folder
- `previous_analyses/`: Archive of past analyses

### Analysis Year Folders
- `vector_data/`: Contains all vector files
  - `points/`: Point data files (e.g., sampling points)
  - `polygons/`: Polygon data files (e.g., land cover boundaries)
- `csv_data/`: Contains all CSV files
  - `raw/`: Original CSV files from data collection
  - `processed/`: Processed and merged CSV files
- `analysis_results/`: Contains analysis outputs
  - `figures/`: Generated plots and visualizations
  - `reports/`: Analysis reports and summaries

## Setup Instructions

1. Create the OneDrive Folder
   - Log in to your OneDrive account
   - Create a new folder named `temporal_landcover_analysis`
   - Share the folder with project collaborators

2. Set Up Initial Structure
   - Create the main subfolders as shown in the structure above
   - Create a README.md file in the root folder with:
     - Project description
     - Folder structure explanation
     - Access instructions
     - Contact information

3. Configure Local Access
   - Install OneDrive desktop app if not already installed
   - Sync the `temporal_landcover_analysis` folder to your local machine
   - Ensure the sync location is outside the Git repository

## Usage Guidelines

1. File Naming Convention
   - Use descriptive names with date prefixes
   - Example: `20240320_ndvi_analysis_results.csv`

2. Data Organization
   - Keep raw data separate from processed data
   - Maintain consistent folder structure across years
   - Archive completed analyses to `previous_analyses`

3. Collaboration
   - Use OneDrive's sharing features for collaboration
   - Maintain appropriate access levels for different users
   - Document any shared resources or dependencies

4. Backup and Version Control
   - OneDrive provides automatic version history
   - Use meaningful version names for important changes
   - Keep local copies of critical data

## Troubleshooting

1. Sync Issues
   - Check OneDrive status
   - Verify folder permissions
   - Ensure sufficient storage space

2. Access Problems
   - Verify user permissions
   - Check sharing settings
   - Contact project administrator

## Contact
For access to the OneDrive folder or technical support:
- Project Administrator: [Contact Information]
- Technical Support: [Contact Information] 