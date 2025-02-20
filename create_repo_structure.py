import os
import pathlib
import shutil

def create_repo_structure():
    # Print current working directory
    print(f"Current working directory: {os.getcwd()}")
    
    # Define the base directory (current directory)
    base_dir = pathlib.Path.cwd()
    print(f"Base directory: {base_dir}")
    
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
        try:
            full_path = base_dir / dir_path
            full_path.mkdir(parents=True, exist_ok=True)
            (full_path / '.gitkeep').touch()
            print(f"Created directory: {dir_path}")
        except Exception as e:
            print(f"Error creating {dir_path}: {e}")
    
    print("\nChecking for files to move...")
    # Move files to their appropriate locations
    file_moves = {
        'raster_timeseries_vectorizer.py': 'scripts/python/',
        'combine_rasters_colad.ipynb': 'scripts/python/',
        'rename_raster_bands_2013_2023.ipynb': 'scripts/python/',
        'landcover_mask.js': 'scripts/gee/'
    }
    
    for file_name, dest_dir in file_moves.items():
        src_path = base_dir / file_name
        dest_path = base_dir / dest_dir / file_name
        print(f"Checking for {file_name}...")
        if src_path.exists():
            try:
                if src_path.is_dir():
                    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_path, dest_path)
                print(f"Moved {file_name} to {dest_dir}")
            except Exception as e:
                print(f"Error moving {file_name}: {e}")
        else:
            print(f"File not found: {file_name}")

    print("\nFinal directory structure:")
    for path in sorted(pathlib.Path(base_dir).rglob('*')):
        if '.git' not in str(path):
            print(f"{'    ' * (len(path.parts) - len(base_dir.parts))}{path.name}")

if __name__ == '__main__':
    create_repo_structure()