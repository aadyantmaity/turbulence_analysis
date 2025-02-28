import matplotlib.pyplot as plt
import os
import pandas as pd
from mpl_toolkits.basemap import Basemap
import numpy as np


def plot_turbulence_on_map(df, title_prefix, save_dir, svg_status):
    start_year, end_year = 2003, 2026
    chunk_df = df[(df['year'] >= start_year) & (df['year'] < end_year)]

    if chunk_df.empty:
        return

    title = f"{title_prefix} {start_year}-{end_year - 1}"

    if svg_status:
        filename = f"turbulence_map_{start_year}_{end_year - 1}.svg"
    else:
        filename = f"turbulence_map_{start_year}_{end_year - 1}.png"
    filepath = os.path.join(save_dir, filename)

    plt.figure(figsize=(35, 10))

    m = Basemap(projection='merc', llcrnrlat=33, urcrnrlat=35.5,
                llcrnrlon=-119, urcrnrlon=-117, resolution='i')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='white', lake_color='aqua')
    m.shadedrelief()

    smooth = chunk_df[
            chunk_df['turbulence'].str.contains('SM|SMOOTH', na=False) |
            chunk_df['report'].str.contains('SM|SMOOTH', na=False)
        ]
    light_turbulence = chunk_df[
        chunk_df['turbulence'].str.contains('LGT|LIGHT', na=False) |
        chunk_df['report'].str.contains('LGT|LIGHT', na=False)
    ]
    moderate_turbulence = chunk_df[
        chunk_df['turbulence'].str.contains('MOD', na=False) |
        chunk_df['report'].str.contains('MOD', na=False)
    ]
    modsev_turbulence = chunk_df[
        chunk_df['turbulence'].str.contains('MOD-SEV', na=False) |
        chunk_df['report'].str.contains('MOD-SEV', na=False)
    ]
    severe_turbulence = chunk_df[
        chunk_df['turbulence'].str.contains('SEV', na=False) |
        chunk_df['report'].str.contains('SEV', na=False)
    ]

    smooth_color = 'lightsteelblue'
    light_color = 'green'
    moderate_color = 'yellow'
    modsev_color = 'orange'
    severe_color = 'red'

    dot_size = 50
    alpha_value = 0.5

    x, y = m(smooth['lon'].values, smooth['lat'].values)
    m.scatter(x, y, color=smooth_color,
                label='Smooth Conditions (SM | SMOOTH)', alpha=alpha_value, s=dot_size)

    x, y = m(light_turbulence['lon'].values,
                light_turbulence['lat'].values)
    m.scatter(x, y, color=light_color,
                label='Light Turbulence (LGT)', alpha=alpha_value, s=dot_size)

    x, y = m(moderate_turbulence['lon'].values,
                moderate_turbulence['lat'].values)
    m.scatter(x, y, color=moderate_color,
                label='Moderate Turbulence (MOD)', alpha=alpha_value, s=dot_size)

    x, y = m(modsev_turbulence['lon'].values,
                modsev_turbulence['lat'].values)
    m.scatter(x, y, color=modsev_color,
                label='Moderate-Severe Turbulence (MOD)', alpha=alpha_value, s=dot_size)

    x, y = m(severe_turbulence['lon'].values,
                severe_turbulence['lat'].values)
    m.scatter(x, y, color=severe_color,
                label='Severe Turbulence (SEV)', alpha=alpha_value, s=dot_size)

    airports = chunk_df['report'].str[:3].unique()
    airport_coords = {
        'LAX': (33.9416, -118.4085),
        'BUR': (34.2007, -118.3581),
        'LGB': (33.8177, -118.1516),
        'EMT': (34.086, -118.035),
    }

    for airport, (lat, lon) in airport_coords.items():
        if airport in airports:
            x, y = m(lon, lat)
            m.plot(x, y, marker='o', color='blue', markersize=10)
            plt.text(x, y, airport, fontsize=12,
                     ha='left', va='bottom', color='blue')

    plt.title(title)
    plt.legend(loc='upper right')

    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    print(f"Saved plot: {filepath}")
    plt.close()


def plot_turbulence_for_dec30_to_jan8(df, title_prefix, save_dir, svg_status):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)

    start_date = pd.Timestamp('2025-01-06')
    end_date = pd.Timestamp('2025-01-08 23:59:59')
    chunk_df_jan6_jan8 = df[(df['valid'] >= start_date)
                            & (df['valid'] <= end_date)]

    if not chunk_df_jan6_jan8.empty:
        title = f"{title_prefix} Jan 6 - Jan 8"

        if svg_status:
            filename = "turbulence_map_jan6_jan8.svg"
        else:
            filename = "turbulence_map_jan6_jan8.png"
        filepath = os.path.join(save_dir, filename)

        plt.figure(figsize=(35, 10))

        m = Basemap(projection='merc', llcrnrlat=32.5, urcrnrlat=35.5,
                    llcrnrlon=-120, urcrnrlon=-116, resolution='i')
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
        m.drawmapboundary(fill_color='aqua')
        m.fillcontinents(color='white', lake_color='aqua')
        m.shadedrelief()

        smooth = chunk_df_jan6_jan8[
            chunk_df_jan6_jan8['turbulence'].str.contains('SM|SMOOTH', na=False) |
            chunk_df_jan6_jan8['report'].str.contains('SM|SMOOTH', na=False)
        ]
        light_turbulence = chunk_df_jan6_jan8[
            chunk_df_jan6_jan8['turbulence'].str.contains('LGT|LIGHT', na=False) |
            chunk_df_jan6_jan8['report'].str.contains('LGT|LIGHT', na=False)
        ]
        moderate_turbulence = chunk_df_jan6_jan8[
            chunk_df_jan6_jan8['turbulence'].str.contains('MOD', na=False) |
            chunk_df_jan6_jan8['report'].str.contains('MOD', na=False)
        ]
        modsev_turbulence = chunk_df_jan6_jan8[
            chunk_df_jan6_jan8['turbulence'].str.contains('MOD-SEV', na=False) |
            chunk_df_jan6_jan8['report'].str.contains('MOD-SEV', na=False)
        ]
        severe_turbulence = chunk_df_jan6_jan8[
            chunk_df_jan6_jan8['turbulence'].str.contains('SEV', na=False) |
            chunk_df_jan6_jan8['report'].str.contains('SEV', na=False)
        ]

        smooth_color = 'lightsteelblue'
        light_color = 'green'
        moderate_color = 'yellow'
        modsev_color = 'orange'
        severe_color = 'red'

        dot_size = 50
        alpha_value = 0.5

        x, y = m(smooth['lon'].values, smooth['lat'].values)
        m.scatter(x, y, color=smooth_color,
                  label='Smooth Conditions (SM | SMOOTH)', alpha=alpha_value, s=dot_size)

        x, y = m(light_turbulence['lon'].values,
                 light_turbulence['lat'].values)
        m.scatter(x, y, color=light_color,
                  label='Light Turbulence (LGT)', alpha=alpha_value, s=dot_size)

        x, y = m(moderate_turbulence['lon'].values,
                 moderate_turbulence['lat'].values)
        m.scatter(x, y, color=moderate_color,
                  label='Moderate Turbulence (MOD)', alpha=alpha_value, s=dot_size)

        x, y = m(modsev_turbulence['lon'].values,
                 modsev_turbulence['lat'].values)
        m.scatter(x, y, color=modsev_color,
                  label='Moderate-Severe Turbulence (MOD)', alpha=alpha_value, s=dot_size)

        x, y = m(severe_turbulence['lon'].values,
                 severe_turbulence['lat'].values)
        m.scatter(x, y, color=severe_color,
                  label='Severe Turbulence (SEV)', alpha=alpha_value, s=dot_size)

        airports = chunk_df_jan6_jan8['report'].str[:3].unique()
        airport_coords = {
            'LAX': (33.9416, -118.4085),
            'BUR': (34.2007, -118.3581),
            'LGB': (33.8177, -118.1516),
            'EMT': (34.086, -118.035),
        }

        for airport, (lat, lon) in airport_coords.items():
            if airport in airports:
                x, y = m(lon, lat)
                m.plot(x, y, marker='^', color='blue', markersize=5)
                plt.text(x, y, airport, fontsize=12,
                         ha='left', va='bottom', color='blue')

        plt.title(title)
        plt.legend(loc='upper right')

        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
        plt.close()

    start_date = pd.Timestamp('2024-12-30')
    end_date = pd.Timestamp('2025-01-05 23:59:59')
    chunk_df_dec30_jan5 = df[(df['valid'] >= start_date)
                             & (df['valid'] <= end_date)]

    if not chunk_df_dec30_jan5.empty:
        title = f"{title_prefix} Dec 30 - Jan 5"

        if svg_status:
            filename = "turbulence_map_dec30_jan5.svg"
        else:
            filename = "turbulence_map_dec30_jan5.png"
        filepath = os.path.join(save_dir, filename)

        plt.figure(figsize=(35, 10))

        m = Basemap(projection='merc', llcrnrlat=32.5, urcrnrlat=35.5,
                    llcrnrlon=-120, urcrnrlon=-116, resolution='i')
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
        m.drawmapboundary(fill_color='aqua')
        m.fillcontinents(color='white', lake_color='aqua')
        m.shadedrelief()

        smooth = chunk_df_dec30_jan5[
            chunk_df_dec30_jan5['turbulence'].str.contains('SM|SMOOTH', na=False) |
            chunk_df_dec30_jan5['report'].str.contains('SM|SMOOTH', na=False)
        ]
        light_turbulence = chunk_df_dec30_jan5[
            chunk_df_dec30_jan5['turbulence'].str.contains('LGT|LIGHT', na=False) |
            chunk_df_dec30_jan5['report'].str.contains('LGT|LIGHT', na=False)
        ]
        moderate_turbulence = chunk_df_dec30_jan5[
            chunk_df_dec30_jan5['turbulence'].str.contains('MOD', na=False) |
            chunk_df_dec30_jan5['report'].str.contains('MOD', na=False)
        ]
        modsev_turbulence = chunk_df_dec30_jan5[
            chunk_df_dec30_jan5['turbulence'].str.contains('MOD-SEV', na=False) |
            chunk_df_dec30_jan5['report'].str.contains('MOD-SEV', na=False)
        ]
        severe_turbulence = chunk_df_dec30_jan5[
            chunk_df_dec30_jan5['turbulence'].str.contains('SEV', na=False) |
            chunk_df_dec30_jan5['report'].str.contains('SEV', na=False)
        ]

        smooth_color = 'lightsteelblue'
        light_color = 'green'
        moderate_color = 'yellow'
        modsev_color = 'orange'
        severe_color = 'red'

        dot_size = 50
        alpha_value = 0.3

        x, y = m(smooth['lon'].values, smooth['lat'].values)
        m.scatter(x, y, color=smooth_color,
                  label='Smooth Conditions (SM | SMOOTH)', alpha=alpha_value, s=dot_size)

        x, y = m(light_turbulence['lon'].values,
                 light_turbulence['lat'].values)
        m.scatter(x, y, color=light_color,
                  label='Light Turbulence (LGT)', alpha=alpha_value, s=dot_size)

        x, y = m(moderate_turbulence['lon'].values,
                 moderate_turbulence['lat'].values)
        m.scatter(x, y, color=moderate_color,
                  label='Moderate Turbulence (MOD)', alpha=alpha_value, s=dot_size)

        x, y = m(modsev_turbulence['lon'].values,
                 modsev_turbulence['lat'].values)
        m.scatter(x, y, color=modsev_color,
                  label='Moderate-Severe Turbulence (MOD)', alpha=alpha_value, s=dot_size)

        x, y = m(severe_turbulence['lon'].values,
                 severe_turbulence['lat'].values)
        m.scatter(x, y, color=severe_color,
                  label='Severe Turbulence (SEV)', alpha=alpha_value, s=dot_size)

        airports = chunk_df_dec30_jan5['report'].str[:3].unique()
        airport_coords = {
            'LAX': (33.9416, -118.4085),
            'BUR': (34.2007, -118.3581),
            'LGB': (33.8177, -118.1516),
            'EMT': (34.086, -118.035),
        }

        for airport, (lat, lon) in airport_coords.items():
            if airport in airports:
                x, y = m(lon, lat)
                m.plot(x, y, marker='^', color='blue', markersize=5)
                plt.text(x, y, airport, fontsize=12,
                         ha='left', va='bottom', color='blue')

        plt.title(title)
        plt.legend(loc='upper right')

        plt.savefig(filepath, dpi=100, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
        plt.close()
