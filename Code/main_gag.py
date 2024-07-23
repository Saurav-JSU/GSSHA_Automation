import gssha_automation_gag
from datetime import datetime

def main():
    # Paths to be updated by user
    shapefile_path = 'path/to/Galveston_poly.shp'
    begin_date_str = '20080911'
    end_date_str = '20080915'
    output_gag_path = 'path/to/file1.gag'
    dataset = 'DAYMET'  # Options: 'DAYMET', 'ERA5', 'PRISM'

    # Convert date strings to datetime objects
    begin_date = datetime.strptime(begin_date_str, '%Y%m%d')
    end_date = datetime.strptime(end_date_str, '%Y%m%d')

    # Step 1: Get bounds from shapefile
    bounds, original_crs = gssha_automation_gag.get_bounds_from_shapefile(shapefile_path)

    # Step 2: Create bounding box
    bounding_box = gssha_automation_gag.create_bounding_box(bounds)

    # Step 3: Get grid centers
    grid_centers = gssha_automation_gag.get_grid_centers(bounding_box)

    # Step 4: Extract precipitation data
    precipitation_data = gssha_automation_gag.extract_precipitation_data(grid_centers, begin_date, end_date, dataset)

    # Step 5: Convert to .gag format
    gssha_automation_gag.convert_to_gag(grid_centers, precipitation_data, output_gag_path, begin_date, end_date, original_crs)

if __name__ == "__main__":
    main()