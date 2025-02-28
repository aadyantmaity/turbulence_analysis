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

    m = Basemap(projection='merc', llcrnrlat=33.5, urcrnrlat=34.5, llcrnrlon=-119, urcrnrlon=-117, resolution='i')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    m.drawmapboundary(fill_color='aqua')
    m.fillcontinents(color='white', lake_color='aqua')
    m.shadedrelief()

    lon = np.linspace(-119, -117, 100)
    lat = np.linspace(33.5, 34.5, 100)
    lon, lat = np.meshgrid(lon, lat)
    x, y = m(lon, lat)

    mod_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD', na=False)]
    sev_turbulence = chunk_df[chunk_df['turbulence'].str.contains('SEV', na=False)]
    combined_turbulence = chunk_df[chunk_df['turbulence'].str.contains('MOD-SEV', na=False)]

    mod_color = 'green'
    sev_color = 'red'
    combined_color = 'orange'

    dot_size = 50

    x, y = m(mod_turbulence['lon'].values, mod_turbulence['lat'].values)
    m.scatter(x, y, color=mod_color, label='Moderate Turbulence (MOD)', alpha=0.7, s=dot_size)

    x, y = m(sev_turbulence['lon'].values, sev_turbulence['lat'].values)
    m.scatter(x, y, color=sev_color, label='Severe Turbulence (SEV)', alpha=0.7, s=dot_size)

    x, y = m(combined_turbulence['lon'].values, combined_turbulence['lat'].values)
    m.scatter(x, y, color=combined_color, label='Moderate-Severe Turbulence (MOD-SEV)', alpha=0.7, s=dot_size)

    airports = chunk_df['report'].str[:3].unique()
    airport_coords = {
        'LAX': (33.9416, -118.4085),
        'BUR': (34.2007, -118.3581),
        'LGB': (33.8177, -118.1516),
        'VNY': (34.2097, -118.4892),
        'SMO': (34.0158, -118.4500),
        'EMT': (34.086, -118.035),
        'TOA': (33.8034, -118.3396),
        'WHP': (34.2593, -118.4134)
    }

    for airport, (lat, lon) in airport_coords.items():
        if airport in airports:
            x, y = m(lon, lat)
            m.plot(x, y, marker='o', color='blue', markersize=10)
            plt.text(x, y, airport, fontsize=12, ha='left', va='bottom', color='blue')

    plt.title(title)
    plt.legend(loc='upper right')

    plt.savefig(filepath, dpi=100, bbox_inches='tight')
    print(f"Saved plot: {filepath}")
    plt.close()