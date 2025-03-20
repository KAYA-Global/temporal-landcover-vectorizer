import os
import shutil
from pathlib import Path

def create_directory_structure(base_path):
    """Create the directory structure in OneDrive."""
    directories = [
        'analysis_2024/vector_data/polygons',
        'analysis_2024/csv_data/raw/biomass',
        'analysis_2024/csv_data/raw/ndfi',
        'analysis_2024/csv_data/processed/ndvi',
        'analysis_2024/analysis_results/figures',
        'analysis_2024/analysis_results/reports',
        'analysis_2024/analysis_results/final_outputs'
    ]
    
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {directory}")
        except Exception as e:
            print(f"Error creating directory {directory}: {str(e)}")

def copy_readme(source_dir, target_dir):
    """Copy the README template to the OneDrive folder."""
    try:
        source_file = os.path.join(source_dir, 'docs', 'onedrive_readme_template.md')
        target_file = os.path.join(target_dir, 'README.md')
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            print(f"Copied: README.md to OneDrive folder")
    except Exception as e:
        print(f"Error copying README: {str(e)}")

def organize_files(source_path, target_path):
    """Organize files from source to target directory."""
    try:
        # Vector data
        source_file = os.path.join(source_path, 'extracted_polygons.gpkg')
        target_file = os.path.join(target_path, 'analysis_2024/vector_data/polygons/extracted_polygons.gpkg')
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            print(f"Copied: extracted_polygons.gpkg")
        
        # Raw biomass data
        for file in os.listdir(os.path.join(source_path, 'csv')):
            if file.startswith('biomass_Area_') and file.endswith('_vectorized.csv'):
                source_file = os.path.join(source_path, 'csv', file)
                target_file = os.path.join(target_path, 'analysis_2024/csv_data/raw/biomass', file)
                shutil.copy2(source_file, target_file)
                print(f"Copied: {file}")
        
        # Raw NDFI data
        for file in os.listdir(os.path.join(source_path, 'csv')):
            if file.startswith('ndfi_Area_') and file.endswith('_vectorized.csv'):
                source_file = os.path.join(source_path, 'csv', file)
                target_file = os.path.join(target_path, 'analysis_2024/csv_data/raw/ndfi', file)
                shutil.copy2(source_file, target_file)
                print(f"Copied: {file}")
        
        # Processed NDVI data
        for file in os.listdir(os.path.join(source_path, 'csv')):
            if file.startswith('NDVI_Merged_Area_'):
                source_file = os.path.join(source_path, 'csv', file)
                target_file = os.path.join(target_path, 'analysis_2024/csv_data/processed/ndvi', file)
                shutil.copy2(source_file, target_file)
                print(f"Copied: {file}")
        
        # Final output
        source_file = os.path.join(source_path, 'sampled_data_with_coords.csv')
        target_file = os.path.join(target_path, 'analysis_2024/analysis_results/final_outputs/sampled_data_with_coords.csv')
        if os.path.exists(source_file):
            shutil.copy2(source_file, target_file)
            print(f"Copied: sampled_data_with_coords.csv")
            
    except Exception as e:
        print(f"Error during file organization: {str(e)}")

def main():
    # Get repository root directory
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Source path (current data folder)
    source_path = os.path.join(repo_root, 'data', 'landcover_analysis_2024')
    
    # Target path (OneDrive folder)
    target_path = r"C:\Users\galag\KAYA Climate Solutions GmbH\Climate - Documents\General\Map projects\Wirong\Temporal Land Cover Analysis"
    
    # Verify paths exist
    if not os.path.exists(source_path):
        print(f"Error: Source path does not exist: {source_path}")
        return
    
    if not os.path.exists(target_path):
        print(f"Error: Target path does not exist: {target_path}")
        return
    
    print(f"Source path: {source_path}")
    print(f"Target path: {target_path}")
    
    # Create directory structure
    print("\nCreating directory structure...")
    create_directory_structure(target_path)
    
    # Copy README
    print("\nCopying README...")
    copy_readme(repo_root, target_path)
    
    # Organize files
    print("\nOrganizing files...")
    organize_files(source_path, target_path)
    
    print("\nFile organization completed!")

if __name__ == "__main__":
    main()