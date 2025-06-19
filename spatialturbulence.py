import os
import pandas as pd
import gmplot


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
        altitude_df = chunk_df[(chunk_df['fl'] >= alt_min)
                               & (chunk_df['fl'] <= alt_max)]

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
            gmap.scatter(severity_df['lat'],
                         severity_df['lon'], color=color, size=50)

        no_data_df = altitude_df[~altitude_df.index.isin(plotted_indices)]
        gmap.scatter(no_data_df['lat'],
                     no_data_df['lon'], color='gray', size=50)


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
        altitude_df = chunk_df[(chunk_df['fl'] >= alt_min)
                               & (chunk_df['fl'] <= alt_max)]

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
            gmap.scatter(severity_df['lat'],
                         severity_df['lon'], color=color, size=50)

        no_data_df = altitude_df[~altitude_df.index.isin(plotted_indices)]
        gmap.scatter(no_data_df['lat'],
                     no_data_df['lon'], color='gray', size=50)


def plot_turbulence_for_jan6_to_jan9_google_maps_altitude_hourblocks(df, title_prefix, save_dir):
    """
    For each altitude range, generate Google Maps plots for Jan 6-9,
    with each plot showing turbulence reports for a specific altitude and a 3-hour block.
    """
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

    # Add a column for 3-hour block (0-3, 3-6, ..., 21-24)
    chunk_df['hour_block'] = chunk_df['valid'].dt.hour // 3 * 3
    chunk_df['block_label'] = chunk_df['hour_block'].astype(
        str) + '-' + (chunk_df['hour_block'] + 3).astype(str)

    for alt_label, (alt_min, alt_max) in altitude_ranges.items():
        altitude_df = chunk_df[(chunk_df['fl'] >= alt_min)
                               & (chunk_df['fl'] <= alt_max)]
        if altitude_df.empty:
            continue

        # For each day and each 3-hour block
        for date in altitude_df['valid'].dt.date.unique():
            day_df = altitude_df[altitude_df['valid'].dt.date == date]
            for block in sorted(day_df['hour_block'].unique()):
                block_df = day_df[day_df['hour_block'] == block]
                if block_df.empty:
                    continue

                block_start = f"{block:02d}:00"
                block_end = f"{(block+3)%24:02d}:00"
                block_label = f"{block:02d}-{(block+3)%24:02d}"
                date_str = pd.Timestamp(date).strftime('%Y%m%d')
                title = f"{title_prefix} {alt_label} {date} {block_label} (Jan 6 - Jan 9)"
                filename = f"turbulence_map_{alt_label.replace(' ', '_').replace('-', '_')}_{date_str}_block_{block_label}_jan6_jan9.html"
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
                    severity_df = block_df[~block_df.index.isin(plotted_indices) &
                                           block_df['turbulence'].str.contains('|'.join(patterns), na=False)]
                    plotted_indices.update(severity_df.index)
                    gmap.scatter(
                        severity_df['lat'], severity_df['lon'], color=color, size=50)

                no_data_df = block_df[~block_df.index.isin(plotted_indices)]
                gmap.scatter(
                    no_data_df['lat'], no_data_df['lon'], color='gray', size=50)

                gmap.draw(filepath)
                print(f"Saved plot: {filepath}")
