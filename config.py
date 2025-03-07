import pandas as pd
import gmplot
import os

df = pd.read_csv("pireps_200311300000_202502132359 (1).csv", low_memory=False)

df.columns = df.columns.str.lower().str.replace(" ", "_")

df['valid'] = pd.to_datetime(df['valid'], format='%Y%m%d%H%M', utc=True)
df['year'] = df['valid'].dt.year

min_year = df['year'].min()
max_year = df['year'].max()

year_chunks = list(range(min_year, max_year + 1, 2))
year_chunks_general = list(range(min_year, max_year))
year_chunks_3 = list(range(min_year, max_year + 1, 3))

def plot_lax_pireps(df, title_prefix, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)

    start_date = pd.Timestamp('2024-12-30')
    end_date = pd.Timestamp('2025-01-09 23:59:59')
    lax_reports = df[(df['valid'] >= start_date) & (df['valid'] <= end_date) & df['report'].str.contains(r'\bLAX\b|\bKLAX\b', na=False)]

    if not lax_reports.empty:
        title = f"{title_prefix} LAX PIREPs"

        filename = "lax_pireps_map.html"
        filepath = os.path.join(save_dir, filename)

        gmap = gmplot.GoogleMapPlotter.from_geocode(
            "Los Angeles", apikey="AIzaSyDp5kKQuO3fJVBMwcWYkPldbq1eDNb9AME")

        gmap.scatter(lax_reports['lat'], lax_reports['lon'], color='blue', size=50)

        gmap.draw(filepath)
        print(f"Saved plot: {filepath}")
        print(f"Number of LAX/KLAX reports plotted: {lax_reports.shape[0]}")

        csv_filename = "lax_pireps_unique_coords.csv"
        csv_filepath = os.path.join(save_dir, csv_filename)
        lax_reports.drop_duplicates(subset=['lat', 'lon']).to_csv(csv_filepath, index=False)
        print(f"Saved unique LAX/KLAX reports with unique coordinates to CSV: {csv_filepath}")

def plot_bur_pireps(df, title_prefix, save_dir):
    df['valid'] = pd.to_datetime(df['valid']).dt.tz_localize(None)

    start_date = pd.Timestamp('2024-12-30')
    end_date = pd.Timestamp('2025-01-09 23:59:59')
    bur_reports = df[(df['valid'] >= start_date) & (df['valid'] <= end_date) & df['report'].str.contains(r'\bBUR\b|\bKBUR\b', na=False)]

    if not bur_reports.empty:
        title = f"{title_prefix} BUR PIREPs"

        filename = "bur_pireps_map.html"
        filepath = os.path.join(save_dir, filename)

        gmap = gmplot.GoogleMapPlotter.from_geocode(
            "Los Angeles", apikey="AIzaSyDp5kKQuO3fJVBMwcWYkPldbq1eDNb9AME")

        gmap.scatter(bur_reports['lat'], bur_reports['lon'], color='blue', size=50)

        gmap.draw(filepath)
        print(f"Saved plot: {filepath}")
        print(f"Number of BUR/KBUR reports plotted: {bur_reports.shape[0]}")
        csv_filename = "bur_pireps.csv"
        csv_filename2 = "bur_pireps_unique_coords.csv"
        csv_filepath2 = os.path.join(save_dir, csv_filename2)
        csv_filepath = os.path.join(save_dir, csv_filename)

        bur_reports.to_csv(csv_filepath, index=False)
        bur_reports.drop_duplicates(subset=['lat', 'lon']).to_csv(csv_filepath2, index=False)
        print(f"Saved unique BUR/KBUR reports with unique coordinates to CSV: {csv_filepath2}")
