# GSSHA Automation Scripts

## Overview

This repository contains scripts to automate the extraction and conversion of precipitation and time series data for use in GSSHA (Gridded Surface Subsurface Hydrologic Analysis) models. The scripts handle shapefile processing, data extraction from various datasets, and conversion to the appropriate formats required by GSSHA.

## Features

### GSSHA .gag Automation
- **Shapefile Processing**: Extracts bounds and converts CRS.
- **Precipitation Data Extraction**: Retrieves data from datasets like ERA5, DAYMET, and PRISM.
- **GAG File Conversion**: Converts extracted data to .gag format.

### GSSHA .xys Automation
- **JSON to CSV Conversion**: Converts time series JSON files from the Coastal Emergency Risks Assessment (CERA) platform into CSV format, extracting essential data.
- **CSV to XYS Conversion**: Processes the CSV files to create XYS formatted files for GSSHA modeling.
- **Geospatial Operations**: Splits the study area shapefile by contour lines, preparing it for further hydrologic analysis in GSSHA.

## Directory Structure

- `Code/`
  - Contains all the Python scripts for the automation processes.
- `Data/`
  - Contains all input data, including time series JSON files and intermediate CSV files.
  - `CERA_timeseries_json/`
    - Directory where raw JSON data from CERA is stored.
  - `CERA_timeseries_csv/`
    - Directory where converted CSV files are stored.
- `Results/`
  - Contains output data from the processing scripts.
  - `CERA_timeseries_xys/`
    - Directory where the XYS files are saved for GSSHA.
  - `shp_to_GSSHA/`
    - Directory where the split shapefiles are saved for use in GSSHA.
- `Shapefile/`
  - Contains shapefiles used for geospatial operations.
  - `CERA_Shapefile/Max_elev/`
    - Directory for max elevation shapefiles from CERA.
  - `Study_area_Shapefile/`
    - Directory for study area shapefiles.

## Instructions for Use

### GSSHA .gag Automation

1. **Shapefile Preparation**: Provide the shapefile of the GSSHA study area (e.g., your watershed or boundary).
2. **Set Parameters**: Specify the time and date range for the model and choose the dataset (ERA5, DAYMET, or PRISM).
3. **Ensure Correct Paths**: Update the paths and parameters in the `main_gag.py` script according to your setup.
4. **Run the Main Script**: Execute the `main_gag.py` script to extract precipitation data and convert it to GAG format.

### GSSHA .xys Automation

1. **Data Preparation**: Download the time series data from the CERA platform and place the folders into the `Data/CERA_timeseries_json` directory.
2. **Ensure Correct Paths**: Update the paths in the `main_xys.py` script according to your directory structure.
3. **Run the Main Script**: Execute the `main_xys.py` script to perform the conversion and processing steps. This will generate the required CSV and XYS files and split the study area by contours.

## Notes

- You must have the Earth Engine API installed and authenticated with Google Earth Engine to run the .gag automation scripts.
- The output GAG file will be saved at the specified location.
- The script handles macOS-specific file naming conventions where folders with the same name are suffixed with `-2`, `-3`, etc. The first file won't have any suffixes which this code handles automatically.
- The max elevation shapefiles should be stored in the `Shapefile/CERA_Shapefile/Max_elev/` directory or any preferred location, updating the path accordingly.
- All timeseries folders should be placed in one main directory. The code processes the entire folder structure, so there is no need to manually copy individual JSON files.

## Requirements

- Python 3.x
- Pandas
- GeoPandas
- Earth Engine API
- Pyproj
- Matplotlib

## Important Reminder

Remember to add the following line at the end of the `.prj` file made in WMS:

```
PRECIP_FILE "\\....location as in other files\{file_name_of.gag_file}"
RAIN_INV_DISTANCE
```
