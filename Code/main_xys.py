import gssha_automatiion_xys

def main():
    # Paths to be updated by user
    input_directory = 'Data/CERA_timeseries_json'  # Path where CERA timeseries JSON folders are stored
    output_directory_csv = 'Data/CERA_timeseries_csv'  # Path where CSV files will be saved
    output_directory_xys = 'Results/CERA_timeseries_xys'  # Path where XYS files will be saved
    contours_fp = 'Shapefile/CERA_Shapefile/Max_elev/maxelev.shp'  # Path to the max elevation shapefile
    study_area_fp = 'Shapefile/Study_area_Shapefile/Galveston_poly.shp'  # Path to the study area shapefile
    output_fp_shapefile = 'Results/shp_to_GSSHA'  # Path where the split shapefiles will be saved

    # Instruction for Users:
    # This script is designed for macOS, which automatically handles files downloaded from CERA by adding suffixes as the name of folders are same.
    # like -2, -3 to folders with the same latitude and longitude names (The first file won't have suffix; the code considers that). 
    # This script accounts for these suffixes.
    
    # The maxelev shapefile should be stored in the Shapefile folder or any directory you prefer, just update the path accordingly.
    
    # All the timeseries folders should be placed in one main directory. You do not need to manually copy the JSON files.
    # You can simply copy and paste the entire folders created by CERA into one main directory. The code will process
    # all the folders and extract the necessary data.
    
    # Step 1: Convert JSON to CSV
    gssha_automatiion_xys.json_to_csv(input_directory, output_directory_csv)

    # Step 2: Convert CSV to XYS
    gssha_automatiion_xys.process_all_csv_in_folder(output_directory_csv, output_directory_xys)

    # Step 3: Split study area by contours
    gssha_automatiion_xys.split_study_area_by_contours(contours_fp, study_area_fp, output_fp_shapefile)

if __name__ == "__main__":
    main()
