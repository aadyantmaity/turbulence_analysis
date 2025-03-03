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
    m.drawmapboundary(fill_color='white')

    m.etopo()

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
    alpha_value = 0.7

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