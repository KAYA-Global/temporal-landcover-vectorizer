import os
import pathlib

def create_repo_structure():
    # Define the base directory (current directory)
    base_dir = pathlib.Path.cwd()
    
    # Define the directory structure
    directories = [
        'scripts',
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
    
    # Move your script if it exists
    script_name = 'raster_timeseries_vectorizer.py'
    if (base_dir / script_name).exists():
        os.rename(
            base_dir / script_name,
            base_dir / 'scripts' / script_name
        )
        print(f"Moved {script_name} to scripts directory")
    
    print("\nRepository structure created successfully!")
    print("\nDirectory structure:")
    for path in sorted(pathlib.Path(base_dir).rglob('*')):
        if '.git' not in str(path):
            print(f"{'    ' * (len(path.parts) - len(base_dir.parts))}{path.name}")

if __name__ == '__main__':
    create_repo_structure()
