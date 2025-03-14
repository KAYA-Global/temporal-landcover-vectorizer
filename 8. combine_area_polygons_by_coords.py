import geopandas as gpd
import pandas as pd
import os

# Input file path
input_gpkg = r"G:\My Drive\earthengine\conversion\vector\extracted_polygons.gpkg"

# Years to process (2015-2021)
years_to_include = [2015, 2017, 2019, 2021]

# Areas to process
areas = [5, 6, 7, 8]

def process_area(area_number):
    # Dictionary to store dataframes for each year
    year_dfs = {}
    
    # Read and process each year's data
    for year in years_to_include:
        layer_name = f"NDVI_JanMay_{year}_Area_{area_number}_polygons"
        try:
            gdf = gpd.read_file(input_gpkg, layer=layer_name)
            
            # Store the complete dataframe for the first year (2015)
            if year == 2015:
                base_gdf = gdf[['x_coord_left', 'y_coord_left', 
                               'y2015', 'x_coord_right', 'y_coord_right', 'geometry']]
            
            # Store year values with coordinates
            year_dfs[year] = gdf[['x_coord_right', 'y_coord_right', f'y{year}']]
            print(f"Successfully processed {layer_name}")
            
        except Exception as e:
            print(f"Error processing layer {layer_name}: {str(e)}")
    
    if not year_dfs:
        print(f"No data found for Area {area_number}")
        return None
    
    # Start with the base dataframe (2015)
    merged_gdf = base_gdf
    
    # Merge each subsequent year's data
    for year in years_to_include[1:]:  # Skip 2015 as it's already in base_gdf
        if year in year_dfs:
            merged_gdf = pd.merge(
                merged_gdf,
                year_dfs[year][['x_coord_right', 'y_coord_right', f'y{year}']],
                on=['x_coord_right', 'y_coord_right'],
                how='outer'
            )
    
    # Reset index to create a clean numeric index
    merged_gdf = merged_gdf.reset_index(drop=True)
    
    # Add fid column
    merged_gdf.insert(0, 'fid', range(len(merged_gdf)))
    
    # Add pixel_id column
    merged_gdf.insert(1, 'pixel_id', range(len(merged_gdf)))
    
    # Ensure columns are in the correct order
    desired_columns = ['fid', 'pixel_id', 'x_coord_left', 'y_coord_left',
                      'y2015', 'y2017', 'y2019', 'y2021',
                      'x_coord_right', 'y_coord_right', 'geometry']
    
    # Reorder columns (excluding any that don't exist)
    existing_columns = [col for col in desired_columns if col in merged_gdf.columns]
    merged_gdf = merged_gdf[existing_columns]
    
    return merged_gdf

# Process each area and save to new files
output_dir = os.path.dirname(input_gpkg)

for area in areas:
    print(f"\nProcessing Area {area}...")
    result_gdf = process_area(area)
    
    if result_gdf is not None:
        output_file = os.path.join(output_dir, f"combined_NDVI_Area_{area}.gpkg")
        result_gdf.to_file(output_file, driver="GPKG")
        print(f"Saved combined data for Area {area} to {output_file}")
        print(f"Number of features: {len(result_gdf)}")

print("\nProcessing complete!")