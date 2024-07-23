import geopandas as gpd
import ee
import pandas as pd
from datetime import datetime, timedelta
import os
from pyproj import Transformer

# Initialize Earth Engine
ee.Initialize()

def create_dir(file_path):
    os.makedirs(file_path, exist_ok=True)

def get_bounds_from_shapefile(shapefile_path):
    """Extracts bounds from a shapefile and converts to EPSG:4326."""
    gdf = gpd.read_file(shapefile_path)
    original_crs = gdf.crs
    gdf = gdf.to_crs(epsg=4326)
    bounds = gdf.total_bounds
    return bounds, original_crs

def create_bounding_box(bounds):
    """Creates a bounding box in GEE."""
    min_lon, min_lat, max_lon, max_lat = bounds
    return ee.Geometry.Rectangle([min_lon, min_lat, max_lon, max_lat])

def get_grid_centers(bounding_box, grid_size_km=10):
    """Generates grid centers within the bounding box."""
    latlon_bounds = bounding_box.bounds().getInfo()
    min_lon, min_lat, max_lon, max_lat = latlon_bounds['coordinates'][0][0][0], latlon_bounds['coordinates'][0][0][1], latlon_bounds['coordinates'][0][2][0], latlon_bounds['coordinates'][0][2][1]
    
    lon_step = grid_size_km / 111.0
    lat_step = grid_size_km / 111.0
    
    lons = [min_lon + i * lon_step for i in range(int((max_lon - min_lon) / lon_step) + 1)]
    lats = [min_lat + i * lat_step for i in range(int((max_lat - min_lat) / lat_step) + 1)]
    
    grid_centers = [(lon, lat) for lon in lons for lat in lats]
    return grid_centers

def is_point_on_land(point):
    """Checks if a point is on land using the SRTM elevation dataset."""
    try:
        land_mask = ee.Image('CGIAR/SRTM90_V4').mask()
        return land_mask.reduceRegion(ee.Reducer.first(), point, 30).getInfo()['elevation'] is not None
    except Exception:
        return False

def extract_precipitation_data(grid_centers, begin_date, end_date, dataset='DAYMET'):
    """Extracts precipitation data for grid centers from GEE."""
    ee_dates = [begin_date + timedelta(days=i) for i in range((end_date - begin_date).days + 1)]
    precipitation_data = []

    for lon, lat in grid_centers:
        point = ee.Geometry.Point([lon, lat])
        if not is_point_on_land(point):
            continue  # Skip points in the ocean
        
        if dataset == 'ERA5':
            image_collection = ee.ImageCollection('ECMWF/ERA5/DAILY').select('total_precipitation')
            conversion_factor = 1000 / 24  # Convert from m/day to mm/hr
        elif dataset == 'DAYMET':
            image_collection = ee.ImageCollection('NASA/ORNL/DAYMET_V4').select('prcp')
            conversion_factor = 1 / 24  # Convert from mm/day to mm/hr
        elif dataset == 'PRISM':
            image_collection = ee.ImageCollection('OREGONSTATE/PRISM/AN81d').select('ppt')
            conversion_factor = 1 / 24  # Convert from mm/day to mm/hr

        for date in ee_dates:
            date_str = date.strftime('%Y-%m-%d')
            image = image_collection.filterDate(date_str).first()
            if image:
                precipitation = image.reduceRegion(ee.Reducer.mean(), point, 1000).getInfo()
                precipitation_value = precipitation.get('total_precipitation' if dataset == 'ERA5' else 'prcp' if dataset == 'DAYMET' else 'ppt', 0) or 0
                precipitation_data.append({
                    'date': date.strftime('%Y%m%d'),
                    'lon': lon,
                    'lat': lat,
                    'precipitation': precipitation_value * conversion_factor
                })

    return pd.DataFrame(precipitation_data)

def convert_to_gag(grid_centers, precipitation_data, output_gag_path, begin_date, end_date, original_crs):
    """Converts precipitation data to .gag format for GSSHA."""
    transformer = Transformer.from_crs("EPSG:4326", original_crs, always_xy=True)
    
    with open(output_gag_path, 'w') as gag_file:
        gag_file.write('EVENT "Rain Gage"\n')
        gag_file.write(f'NRGAG {len(grid_centers)}\n')
        
        date_range = pd.date_range(start=begin_date, end=end_date, freq='H')
        gag_file.write(f'NRPDS {len(date_range)}\n')
        
        for i, (lon, lat) in enumerate(grid_centers):
            transformed_lon, transformed_lat = transformer.transform(lon, lat)
            gag_file.write(f'COORD {transformed_lon} {transformed_lat} "Gage{i+1}"\n')
        
        for date in date_range:
            date_str = date.strftime("%Y %m %d %H %M")
            line = f'GAGES {date_str}'
            for lon, lat in grid_centers:
                precip_df = precipitation_data[(precipitation_data['date'] == date.strftime('%Y%m%d')) & 
                                               (precipitation_data['lon'] == lon) & 
                                               (precipitation_data['lat'] == lat)]
                if not precip_df.empty:
                    precipitation = precip_df['precipitation'].values[0]
                    line += f' {precipitation:.3f}'
                else:
                    line += ' 0.000'
            line += '\n'
            gag_file.write(line)