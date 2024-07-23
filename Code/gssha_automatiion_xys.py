import os
import json
import pandas as pd
import shutil
import geopandas as gpd
import matplotlib.pyplot as plt

def create_dir(file_path):
    os.makedirs(file_path, exist_ok=True)

def extract_forecast_data(forecast_data):
    """Extracts time_UTC and value_ft from forecast_data and converts value_ft to meters."""
    extracted_data = [{'Time': entry['time_UTC'], 'Water_height': float(entry['value_ft']) * 0.3048} for entry in forecast_data]
    return extracted_data

def get_subfolder_number(subfolder_name):
    """Extracts the number at the end of the subfolder name or assigns 1 if none exists."""
    parts = subfolder_name.rsplit('-', 1)
    if len(parts) > 1 and parts[-1].isdigit():
        return parts[-1]
    return '1'

def json_to_csv(input_dir, output_dir):
    """Converts JSON files to CSV, extracts necessary data, and saves to output directory."""
    create_dir(output_dir)

    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith('.json'):
                json_filepath = os.path.join(root, file)
                with open(json_filepath, 'r') as f:
                    data = json.load(f)

                forecast_data = data.get('forecast_data', [])
                extracted_data = extract_forecast_data(forecast_data)
                df = pd.DataFrame(extracted_data)

                subfolder_name = os.path.basename(root)
                subfolder_number = get_subfolder_number(subfolder_name)
                
                csv_filename = f"Curve-{subfolder_number}.csv"
                csv_filepath = os.path.join(output_dir, csv_filename)

                df.to_csv(csv_filepath, index=False)
                print(f"CSV file '{csv_filename}' has been created successfully.")

def filter_and_convert_to_xys(df, curve_name, start_index, xys_path):
    """Filters the dataframe and converts it to an XYS file format."""
    df['Time'] = pd.to_datetime(df['Time'])
    start_row = df[df['Time'].dt.strftime('%I:%M:%S %p') == "12:00:00 AM"]

    if not start_row.empty:
        start_idx = start_row.index[0]
        df = df.loc[start_idx:]

        with open(xys_path, 'w') as file:
            file.write(f'XYS {start_index} 91 "{curve_name}"\n')
            for _, row in df.iterrows():
                file.write(f'"{row["Time"].strftime("%m/%d/%Y %I:%M:%S %p")}" {row["Water_height"]}\n')

def process_all_csv_in_folder(input_folder, output_folder):
    """Processes all CSV files in the input folder and converts them to XYS format."""
    create_dir(output_folder)
    csv_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]

    for i, csv_file in enumerate(csv_files):
        csv_path = os.path.join(input_folder, csv_file)
        curve_name = os.path.splitext(csv_file)[0].replace('-', '')
        xys_file = os.path.join(output_folder, f"{curve_name}.xys")
        curve_df = pd.read_csv(csv_path)

        filter_and_convert_to_xys(curve_df, curve_name, 119 + i, xys_file)

    # Delete all CSV files after processing
    for csv_file in csv_files:
        os.remove(os.path.join(input_folder, csv_file))
    print(f"All CSV files in '{input_folder}' have been deleted.")

def split_study_area_by_contours(contours_fp, study_area_fp, output_fp):
    """Splits the study area by contour lines and saves the result."""
    contours = gpd.read_file(contours_fp)
    study_area = gpd.read_file(study_area_fp)

    if contours.crs != study_area.crs:
        contours = contours.to_crs(study_area.crs)

    split_areas = gpd.overlay(study_area, contours, how='intersection')
    create_dir(output_fp)
    split_areas.to_file(os.path.join(output_fp, 'boundary.shp'))