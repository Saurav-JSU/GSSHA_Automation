## GSSHA Automation XYS

This repository contains a set of scripts designed to automate the processing of time series data from the Coastal Emergency Risks Assessment (CERA) platform and integrate it into GSSHA (Gridded Surface Subsurface Hydrologic Analysis) models. The scripts convert JSON data files to CSV and XYS formats, and perform geospatial operations on study areas using contour lines. The scripts are optimized for macOS environments.

### Features

- **JSON to CSV Conversion**: Converts time series JSON files from the CERA platform into CSV format, extracting essential data.
- **CSV to XYS Conversion**: Processes the CSV files to create XYS formatted files, which are used in GSSHA modeling.
- **Geospatial Operations**: Splits the study area shapefile by contour lines, preparing it for further hydrologic analysis in GSSHA.

### Directory Structure

- `Data/`: Contains all input data, including time series JSON files and intermediate CSV files.
  - `CERA_timeseries_json/`: Directory where raw JSON data from CERA is stored.
  - `CERA_timeseries_csv/`: Directory where converted CSV files are stored.
  - `Water_level/`: Directory for storing processed water level data.
- `Results/`: Contains output data from the processing scripts.
  - `CERA_timeseries_xys/`: Directory where the XYS files are saved.
  - `shp_to_GSSHA/`: Directory where the split shapefiles are saved.
- `Shapefile/`: Contains shapefiles used for geospatial operations.
  - `CERA_Shapefile/Max_elev/`: Directory for the max elevation shapefiles.
  - `Study_area_Shapefile/`: Directory for the study area shapefiles.

### Usage

#### 1. JSON to CSV Conversion

The script `gssha_automatiion_xys.json_to_csv` converts JSON files to CSV format. The JSON files should be placed in the `Data/CERA_timeseries_json` directory. The converted CSV files will be saved in the `Data/CERA_timeseries_csv` directory.

```python
gssha_automatiion_xys.json_to_csv(input_directory, output_directory_csv)
```

#### 2. CSV to XYS Conversion

The script `gssha_automatiion_xys.process_all_csv_in_folder` processes all CSV files in the specified input folder and converts them to XYS format. The output XYS files will be saved in the `Results/CERA_timeseries_xys` directory.

```python
gssha_automatiion_xys.process_all_csv_in_folder(output_directory_csv, output_directory_xys)
```

#### 3. Split Study Area by Contours

The script `gssha_automatiion_xys.split_study_area_by_contours` splits the study area shapefile by contour lines and saves the result. Ensure the contour and study area shapefiles are correctly placed in their respective directories.

```python
gssha_automatiion_xys.split_study_area_by_contours(contours_fp, study_area_fp, output_fp_shapefile)
```

### Instructions for Use

1. **Data Preparation**: Download the time series data from the CERA platform and place the folders (which macOS may automatically name with suffixes like `-1`, `-2`, etc.) into the `Data/CERA_timeseries_json` directory.
2. **Ensure Correct Paths**: Update the paths in the `main.py` script according to your directory structure.
3. **Run the Main Script**: Execute the `main.py` script to perform the conversion and processing steps. This will generate the required CSV and XYS files and split the study area by contours.

```bash
python main.py
```

### Notes

- The script handles macOS-specific file naming conventions where folders with the same name are suffixed with `-1`, `-2`, etc.
- The max elevation shapefiles should be stored in the `Shapefile/CERA_Shapefile/Max_elev/` directory or any preferred location, updating the path accordingly.
- All timeseries folders should be placed in one main directory. The code processes the entire folder structure, so there is no need to manually copy individual JSON files.

### Requirements

- Python 3.x
- Pandas
- GeoPandas
- Matplotlib

### Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue if you have any suggestions or improvements.
