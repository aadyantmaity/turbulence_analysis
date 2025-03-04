import matplotlib.pyplot as plt
import os
import pandas as pd
from mpl_toolkits.basemap import Basemap
import gmplot


def plot_turbulence_for_jan6_to_jan9_google_maps(df, title_prefix, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)

    start_date = pd.Timestamp('2025-01-06')
    end_date = pd.Timestamp('2025-01-09 23:59:59')
    chunk_df_jan6_jan9 = df[(df['valid'] >= start_date)
                            & (df['valid'] <= end_date)]

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

        gmap.scatter(smooth['lat'], smooth['lon'], color='gray', size=50)
        gmap.scatter(no_data['lat'], no_data['lon'], color='white', size=50)
        gmap.scatter(
            light_turbulence['lat'], light_turbulence['lon'], color='green', size=50, label='')
        gmap.scatter(
            moderate_turbulence['lat'], moderate_turbulence['lon'], color='yellow', size=50, label='')
        gmap.scatter(
            modsev_turbulence['lat'], modsev_turbulence['lon'], color='orange', size=50, label='')
        gmap.scatter(
            severe_turbulence['lat'], severe_turbulence['lon'], color='red', size=50, label='')

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

        chunk_df_jan6_jan9[['report', 'turbulence']].to_csv(
            os.path.join(save_dir, "turbulence_data_jan6_jan9.csv"), index=False)


def plot_turbulence_for_dec30_to_jan5_google_maps(df, title_prefix, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)

    start_date = pd.Timestamp('2024-12-30')
    end_date = pd.Timestamp('2025-01-05 23:59:59')
    chunk_df_dec30_jan5 = df[(df['valid'] >= start_date)
                             & (df['valid'] <= end_date)]

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
            ~ chunk_df_dec30_jan5.index.isin(smooth.index)
        ]

        gmap.scatter(smooth['lat'], smooth['lon'],
                     color='gray', size=50, label='')
        gmap.scatter(no_data['lat'], no_data['lon'],
                     color='white', size=50, label='')
        gmap.scatter(
            light_turbulence['lat'], light_turbulence['lon'], color='green', size=50, label='')
        gmap.scatter(
            moderate_turbulence['lat'], moderate_turbulence['lon'], color='yellow', size=50, label='')
        gmap.scatter(
            modsev_turbulence['lat'], modsev_turbulence['lon'], color='orange', size=50, label='')
        gmap.scatter(
            severe_turbulence['lat'], severe_turbulence['lon'], color='red', size=50, label='')

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

        chunk_df_dec30_jan5[['report', 'turbulence']].to_csv(
            os.path.join(save_dir, "turbulence_data_dec30_jan5.csv"), index=False)
