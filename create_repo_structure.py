import os
import pathlib
import shutil

def create_repo_structure():
    # Define the base directory (current directory)
    base_dir = pathlib.Path.cwd()
    
    # Define the directory structure
    directories = [
        'scripts/python',
        'scripts/gee',
        'data/input/raster',
        'data/output/raster',
        'data/output/vector/points',
        'data/output/vector/polygons',
        'data/output/csv',
        'docs'
    ]
    
    # Create directories
    for dir_path in directories:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        # Create .gitkeep to maintain empty directories in git
        (full_path / '.gitkeep').touch()
        print(f"Created directory: {dir_path}")
    
    # Create initial documentation file
    docs_path = base_dir / 'docs' / 'workflow_documentation.md'
    if not docs_path.exists():
        with open(docs_path, 'w') as f:
            f.write('# Workflow Documentation\n\n')
            f.write('## Overview\n')
            f.write('This document describes the workflow for processing temporal land cover data.\n')
        print("Created workflow documentation file")
    
    # Move files to their appropriate locations
    file_moves = {
        'raster_timeseries_vectorizer.py': 'scripts/python/',
        'combine_rasters_colad.ipynb': 'scripts/python/',
        'rename_raster_bands_2013_2023.ipynb': 'scripts/python/',
        'landcover_mask-js': 'scripts/gee/'
    }
    
    for file_name, dest_dir in file_moves.items():
        src_path = base_dir / file_name
        dest_path = base_dir / dest_dir / file_name
        if src_path.exists():
            if src_path.is_dir():
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dest_path)
            print(f"Moved {file_name} to {dest_dir}")
    
    print("\nRepository structure created successfully!")
    print("\nDirectory structure:")
    for path in sorted(pathlib.Path(base_dir).rglob('*')):
        if '.git' not in str(path):
            print(f"{'    ' * (len(path.parts) - len(base_dir.parts))}{path.name}")

if __name__ == '__main__':
    create_repo_structure()
