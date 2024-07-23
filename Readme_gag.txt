
GSSHA .gag Automation (All code in Code/gssha_automation_gag.py and Code/main_gag.py)

This repository also contains scripts to automate the extraction of precipitation data from Google Earth Engine and convert it into .gag format for GSSHA models. The scripts handle shapefile processing, data extraction from various datasets, and the conversion to GAG format.

Features

	•	Shapefile Processing: Extracts bounds and converts CRS.
	•	Precipitation Data Extraction: Retrieves data from datasets like ERA5, DAYMET, and PRISM.
	•	GAG File Conversion: Converts extracted data to .gag format.

Instructions for Use

	1.	Shapefile Preparation: Provide the shapefile of the GSSHA study area (e.g., your watershed or boundary).
	2.	Set Parameters: Specify the time and date range for the model and choose the dataset (ERA5, DAYMET, or PRISM).
	3.	Ensure Correct Paths: Update the paths and parameters in the main.py script according to your setup.
	4.	Run the Main Script: Execute the main.py script to extract precipitation data and convert it to GAG format.

Notes

	•	You must have the Earth Engine API installed and authenticated with Google Earth Engine to run the scripts.
	•	The output GAG file will be saved at the specified location.

Requirements

	•	Python 3.x
	•	Pandas
	•	GeoPandas
	•	Earth Engine API
	•	Pyproj

ALSO AT LAST REMEMBER TO PUT THIS AT THE END OF .prj FILE MADE IN WMS
PRECIP_FILE "\\....location as in other files\{file_name_of.gag_file}"
RAIN_INV_DISTANCE
