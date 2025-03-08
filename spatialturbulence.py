import matplotlib.pyplot as plt
import os
import pandas as pd
from mpl_toolkits.basemap import Basemap
import gmplot

def plot_turbulence_for_jan6_to_jan9_google_maps(df, title_prefix, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)

    start_date = pd.Timestamp('2025-01-06')
    end_date = pd.Timestamp('2025-01-09 23:59:59')
    chunk_df_jan6_jan9 = df[(df['valid'] >= start_date) & (df['valid'] <= end_date)]

    if not chunk_df_jan6_jan9.empty:
        title = f"{title_prefix} Jan 6 - Jan 9"

        filename = "turbulence_map_jan6_jan9.html"
        filepath = os.path.join(save_dir, filename)

        gmap = gmplot.GoogleMapPlotter.from_geocode(
            "Los Angeles", apikey="AIzaSyDp5kKQuO3fJVBMwcWYkPldbq1eDNb9AME")

        modsev_turbulence = chunk_df_jan6_jan9[
            (chunk_df_jan6_jan9['turbulence'].str.contains(r'\bMOD-SEV\b', na=False) |
             chunk_df_jan6_jan9['report'].str.contains(r'\bMOD-SEV\b', na=False))
        ]

        severe_turbulence = chunk_df_jan6_jan9[
            ~chunk_df_jan6_jan9.index.isin(modsev_turbulence.index) &
            (chunk_df_jan6_jan9['turbulence'].str.contains(r'\bSEVERE\b|\bSEV\b', na=False) |
             chunk_df_jan6_jan9['report'].str.contains(r'\bSEVERE\b|\bSEV\b', na=False))
        ]

        modsev_turbulence = chunk_df_jan6_jan9[
            ~chunk_df_jan6_jan9.index.isin(severe_turbulence.index) &
            (chunk_df_jan6_jan9['turbulence'].str.contains(r'\bMOD-SEV\b', na=False) |
             chunk_df_jan6_jan9['report'].str.contains(r'\bMOD-SEV\b', na=False))
        ]

        moderate_turbulence = chunk_df_jan6_jan9[
            ~chunk_df_jan6_jan9.index.isin(severe_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(modsev_turbulence.index) &
            (chunk_df_jan6_jan9['turbulence'].str.contains(r'\bMOD\b', na=False) |
             chunk_df_jan6_jan9['report'].str.contains(r'\bMOD\b', na=False))
        ]

        light_turbulence = chunk_df_jan6_jan9[
            ~chunk_df_jan6_jan9.index.isin(severe_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(modsev_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(moderate_turbulence.index) &
            (chunk_df_jan6_jan9['turbulence'].str.contains(r'\bLGT\b|\bLIGHT\b', na=False) |
             chunk_df_jan6_jan9['report'].str.contains(r'\bLGT\b|\bLIGHT\b', na=False))
        ]

        smooth = chunk_df_jan6_jan9[
            ~chunk_df_jan6_jan9.index.isin(severe_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(modsev_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(moderate_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(light_turbulence.index) &
            (chunk_df_jan6_jan9['turbulence'].str.contains(r'\bSM\b|\bSMOOTH\b', na=False) |
             chunk_df_jan6_jan9['report'].str.contains(r'\bSM\b|\bSMOOTH\b', na=False))
        ]

        no_data = chunk_df_jan6_jan9[
            ~chunk_df_jan6_jan9.index.isin(severe_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(modsev_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(moderate_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(light_turbulence.index) &
            ~chunk_df_jan6_jan9.index.isin(smooth.index)
        ]

        gmap.scatter(modsev_turbulence['lat'], modsev_turbulence['lon'], color='orange', size=50)
        gmap.scatter(severe_turbulence['lat'], severe_turbulence['lon'], color='red', size=50)
        gmap.scatter(moderate_turbulence['lat'], moderate_turbulence['lon'], color='yellow', size=50)
        gmap.scatter(light_turbulence['lat'], light_turbulence['lon'], color='green', size=50)
        gmap.scatter(smooth['lat'], smooth['lon'], color='gray', size=50)
        gmap.scatter(no_data['lat'], no_data['lon'], color='gray', size=50)

        airports = df['report'].dropna().str.extract(
            r'\b(K?[A-Z]{3})\b')[0].unique()
        airport_coords = {
            'LAX': (33.9416, -118.4085),
            'BUR': (34.2007, -118.3581),
            'LGB': (33.8177, -118.1516),
            'EMT': (34.086, -118.035),
            'VNY': (34.21073, -118.48985),
            'SMO': (34.01582, -118.45131),
        }

        for airport, (lat, lon) in airport_coords.items():
            if airport in airports:
                gmap.marker(lat, lon, color='cyan', label=airport)

        gmap.draw(filepath)
        print(f"Saved plot: {filepath}")

def plot_turbulence_for_dec30_to_jan5_google_maps(df, title_prefix, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)

    start_date = pd.Timestamp('2024-12-30')
    end_date = pd.Timestamp('2025-01-05 23:59:59')
    chunk_df_dec30_jan5 = df[(df['valid'] >= start_date) & (df['valid'] <= end_date)]

    if not chunk_df_dec30_jan5.empty:
        title = f"{title_prefix} Dec 30 - Jan 5"

        filename = "turbulence_map_dec30_jan5.html"
        filepath = os.path.join(save_dir, filename)

        gmap = gmplot.GoogleMapPlotter.from_geocode(
            "Los Angeles", apikey="AIzaSyDp5kKQuO3fJVBMwcWYkPldbq1eDNb9AME")

        modsev_turbulence = chunk_df_dec30_jan5[
            (chunk_df_dec30_jan5['turbulence'].str.contains(r'\bMOD-SEV\b', na=False) |
             chunk_df_dec30_jan5['report'].str.contains(r'\bMOD-SEV\b', na=False))
        ]

        severe_turbulence = chunk_df_dec30_jan5[
            ~chunk_df_dec30_jan5.index.isin(modsev_turbulence.index) &
            (chunk_df_dec30_jan5['turbulence'].str.contains(r'\bSEVERE\b|\bSEV\b', na=False) |
             chunk_df_dec30_jan5['report'].str.contains(r'\bSEVERE\b|\bSEV\b', na=False))
        ]

        modsev_turbulence = chunk_df_dec30_jan5[
            ~chunk_df_dec30_jan5.index.isin(severe_turbulence.index) &
            (chunk_df_dec30_jan5['turbulence'].str.contains(r'\bMOD-SEV\b', na=False) |
             chunk_df_dec30_jan5['report'].str.contains(r'\bMOD-SEV\b', na=False))
        ]

        moderate_turbulence = chunk_df_dec30_jan5[
            ~chunk_df_dec30_jan5.index.isin(severe_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(modsev_turbulence.index) &
            (chunk_df_dec30_jan5['turbulence'].str.contains(r'\bMOD\b', na=False) |
             chunk_df_dec30_jan5['report'].str.contains(r'\bMOD\b', na=False))
        ]

        light_turbulence = chunk_df_dec30_jan5[
            ~chunk_df_dec30_jan5.index.isin(severe_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(modsev_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(moderate_turbulence.index) &
            (chunk_df_dec30_jan5['turbulence'].str.contains(r'\bLGT\b|\bLIGHT\b', na=False) |
             chunk_df_dec30_jan5['report'].str.contains(r'\bLGT\b|\bLIGHT\b', na=False))
        ]

        smooth = chunk_df_dec30_jan5[
            ~chunk_df_dec30_jan5.index.isin(severe_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(modsev_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(moderate_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(light_turbulence.index) &
            (chunk_df_dec30_jan5['turbulence'].str.contains(r'\bSM\b|\bSMOOTH\b', na=False) |
             chunk_df_dec30_jan5['report'].str.contains(r'\bSM\b|\bSMOOTH\b', na=False))
        ]

        no_data = chunk_df_dec30_jan5[
            ~chunk_df_dec30_jan5.index.isin(severe_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(modsev_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(moderate_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(light_turbulence.index) &
            ~chunk_df_dec30_jan5.index.isin(smooth.index)
        ]

        gmap.scatter(modsev_turbulence['lat'], modsev_turbulence['lon'], color='orange', size=50)
        gmap.scatter(severe_turbulence['lat'], severe_turbulence['lon'], color='red', size=50)
        gmap.scatter(moderate_turbulence['lat'], moderate_turbulence['lon'], color='yellow', size=50)
        gmap.scatter(light_turbulence['lat'], light_turbulence['lon'], color='green', size=50)
        gmap.scatter(smooth['lat'], smooth['lon'], color='gray', size=50)
        gmap.scatter(no_data['lat'], no_data['lon'], color='gray', size=50)

        airport_coords = {
            'LAX': (33.9416, -118.4085),
            'BUR': (34.2007, -118.3581),
            'LGB': (33.8177, -118.1516),
            'EMT': (34.086, -118.035),
        }

        for airport, (lat, lon) in airport_coords.items():
            if airport in chunk_df_dec30_jan5['report'].str[:3].unique():
                gmap.marker(lat, lon, color='cyan', label=airport)

        gmap.draw(filepath)
        print(f"Saved plot: {filepath}")

def plot_turbulence_for_jan6_to_jan9_google_maps_altitude(df, title_prefix, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)
    
    start_date = pd.Timestamp('2025-01-06')
    end_date = pd.Timestamp('2025-01-09 23:59:59')
    chunk_df = df[(df['valid'] >= start_date) & (df['valid'] <= end_date)]
    
    altitude_ranges = {
        "0-2000 ft": (0, 2000),
        "2000-4000 ft": (2000, 4000),
        "4000-6000 ft": (4000, 6000),
        "6000-8000 ft": (6000, 8000),
        "8000-12000 ft": (8000, 12000),
        "12000-20000 ft": (12000, 20000)
    }
    
    if chunk_df.empty:
        print("No data available for the given time range.")
        return
    
    for alt_label, (alt_min, alt_max) in altitude_ranges.items():
        altitude_df = chunk_df[(chunk_df['fl'] >= alt_min) & (chunk_df['fl'] <= alt_max)]
        
        if altitude_df.empty:
            continue
        
        title = f"{title_prefix} {alt_label} (Jan 6 - Jan 9)"
        filename = f"turbulence_map_{alt_label.replace(' ', '_').replace('-', '_')}_jan6_jan9.html"
        filepath = os.path.join(save_dir, filename)
        
        gmap = gmplot.GoogleMapPlotter.from_geocode(
            "Los Angeles", apikey="AIzaSyDp5kKQuO3fJVBMwcWYkPldbq1eDNb9AME"
        )
        
        severity_categories = {
            "severe": ("red", [r'\bSEVERE\b', r'\bSEV\b']),
            "mod-sev": ("orange", [r'\bMOD-SEV\b']),
            "moderate": ("yellow", [r'\bMOD\b']),
            "light": ("green", [r'\bLGT\b', r'\bLIGHT\b']),
            "smooth": ("gray", [r'\bSM\b', r'\bSMOOTH\b'])
        }
        
        plotted_indices = set()
        for severity, (color, patterns) in severity_categories.items():
            severity_df = altitude_df[~altitude_df.index.isin(plotted_indices) & 
                                      altitude_df['turbulence'].str.contains('|'.join(patterns), na=False)]
            plotted_indices.update(severity_df.index)
            gmap.scatter(severity_df['lat'], severity_df['lon'], color=color, size=50)
        
        no_data_df = altitude_df[~altitude_df.index.isin(plotted_indices)]
        gmap.scatter(no_data_df['lat'], no_data_df['lon'], color='gray', size=50)
        
        gmap.draw(filepath)
        print(f"Saved plot: {filepath}")

def plot_turbulence_for_dec30_to_jan5_google_maps_altitude(df, title_prefix, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)
    
    start_date = pd.Timestamp('2024-12-30')
    end_date = pd.Timestamp('2025-01-05 23:59:59')
    chunk_df = df[(df['valid'] >= start_date) & (df['valid'] <= end_date)]
    
    altitude_ranges = {
        "0-2000 ft": (0, 2000),
        "2000-4000 ft": (2000, 4000),
        "4000-6000 ft": (4000, 6000),
        "6000-8000 ft": (6000, 8000),
        "8000-12000 ft": (8000, 12000),
        "12000-20000 ft": (12000, 20000)
    }
    
    if chunk_df.empty:
        print("No data available for the given time range.")
        return
    
    for alt_label, (alt_min, alt_max) in altitude_ranges.items():
        altitude_df = chunk_df[(chunk_df['fl'] >= alt_min) & (chunk_df['fl'] <= alt_max)]
        
        if altitude_df.empty:
            continue
        
        title = f"{title_prefix} {alt_label} (Dec 30 - Jan 5)"
        filename = f"turbulence_map_{alt_label.replace(' ', '_').replace('-', '_')}_dec30_jan5.html"
        filepath = os.path.join(save_dir, filename)
        
        gmap = gmplot.GoogleMapPlotter.from_geocode(
            "Los Angeles", apikey="AIzaSyDp5kKQuO3fJVBMwcWYkPldbq1eDNb9AME"
        )
        
        severity_categories = {
            "severe": ("red", [r'\bSEVERE\b', r'\bSEV\b']),
            "mod-sev": ("orange", [r'\bMOD-SEV\b']),
            "moderate": ("yellow", [r'\bMOD\b']),
            "light": ("green", [r'\bLGT\b', r'\bLIGHT\b']),
            "smooth": ("gray", [r'\bSM\b', r'\bSMOOTH\b'])
        }
        
        plotted_indices = set()
        for severity, (color, patterns) in severity_categories.items():
            severity_df = altitude_df[~altitude_df.index.isin(plotted_indices) & 
                                      altitude_df['turbulence'].str.contains('|'.join(patterns), na=False)]
            plotted_indices.update(severity_df.index)
            gmap.scatter(severity_df['lat'], severity_df['lon'], color=color, size=50)
        
        no_data_df = altitude_df[~altitude_df.index.isin(plotted_indices)]
        gmap.scatter(no_data_df['lat'], no_data_df['lon'], color='gray', size=50)
        
        gmap.draw(filepath)
        print(f"Saved plot: {filepath}")
        
def save_pireps_to_csv(df, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)

    start_date = pd.Timestamp('2024-12-30')
    end_date = pd.Timestamp('2025-01-09 23:59:59')
    filtered_df = df[(df['valid'] >= start_date) & (df['valid'] <= end_date)]
    filtered_df_unique = filtered_df.drop_duplicates(subset=['lat', 'lon'])

    if not filtered_df.empty:
        csv_filename = "pireps_dec30_to_jan9.csv"
        csv_new_filename = "pireps_dec30_to_jan9_unique.csv"
        csv_filepath = os.path.join(save_dir, csv_filename)
        csv_filename_unique_filepath = os.path.join(save_dir, csv_new_filename)
        filtered_df.to_csv(csv_filepath, index=False)
        filtered_df_unique.to_csv(csv_filename_unique_filepath, index=False)
        print(f"Saved PIREPs from Dec 30, 2024 to Jan 9, 2025 to CSV: {csv_filepath}")

