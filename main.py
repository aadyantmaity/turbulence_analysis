import os
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
from utils.config import year_chunks, year_chunks_general, year_chunks_3
from utils.preprocessing import preprocess_data
from old_plotting_scripts.santaana import offshoreFilter
from utils.directorycreator import output_dir_svg_spatial_terrain, detailed_general_dir_png, detailed_burbank_dir_png, detailed_offshore_dir_png, general_3year_dir_png, burbank_3year_dir_png, offshore_3year_dir_png, burbank_full_dir_png, general_full_dir_png, offshore_full_dir_png, output_dir_svg_spatial_terrain_altitude

# PREPROCESSING
input_csv = "pireps_200311300000_202502132359 (1).csv"
output_csvs = {
    'preprocessed': "data_csv_files/preprocessed_dataset.csv",
    'burbank_turbulence': "data_csv_files/burbank_turbulence.csv",
    'burbank_turbulence_severe': "data_csv_files/burbank_turbulence_severe.csv",
    'fl_42000_or_above': "data_csv_files/fl_42000_or_above.csv"
}

offshore_flow = offshoreFilter()

df, burbank_turbulence = preprocess_data(input_csv, output_csvs)

# PLOTTING
df['year'] = df['valid'].dt.year
burbank_turbulence.loc[:, 'year'] = burbank_turbulence['valid'].dt.year
offshore_flow['valid'] = pd.to_datetime(offshore_flow['valid'])
offshore_flow['year'] = offshore_flow['valid'].dt.year

min_year = df['year'].min()
max_year = df['year'].max()
year_chunks = list(range(min_year, max_year + 1, 2))
year_chunks_general = list(range(min_year, max_year))
year_chunks_3 = list(range(min_year, max_year + 1, 3))

if __name__ == "__main__":
    from old_plotting_scripts.turbulence3yearchunks import plot_turbulence_by_3year_chunks
    from old_plotting_scripts.turbulencedetailedburbank import plot_detailed_turbulence_burbank
    from old_plotting_scripts.turbulencedetailedgeneral import plot_detailed_turbulence_general
    from old_plotting_scripts.turbulencefull import plot_turbulence_full_range
    from spatialturbulence import plot_turbulence_for_jan6_to_jan9_google_maps, plot_turbulence_for_dec30_to_jan5_google_maps, plot_turbulence_for_jan6_to_jan9_google_maps_altitude, plot_turbulence_for_dec30_to_jan5_google_maps_altitude, save_pireps_to_csv

    # PLOT TURBULENCE FOR DEC 30 to JAN 9
    # plot_turbulence_for_jan6_to_jan9_google_maps(df, "Turbulence Reports", output_dir_svg_spatial_terrain_altitude)
    # plot_turbulence_for_dec30_to_jan5_google_maps(df, "Turbulence Reports", output_dir_svg_spatial_terrain_altitude)
    # plot_turbulence_for_jan6_to_jan9_google_maps_altitude(df, "Turbulence Reports", output_dir_svg_spatial_terrain_altitude)
    # plot_turbulence_for_dec30_to_jan5_google_maps_altitude(df, "Turbulence Reports", output_dir_svg_spatial_terrain_altitude)
    # save_pireps_to_csv(df, output_dir_svg_spatial_terrain)
    
    # png plots

    # PLOT TURBULENCE DETAILED
    # plot_detailed_turbulence_general(df, "Detailed Turbulence Reports", detailed_general_dir_png)
    # plot_detailed_turbulence_burbank(burbank_turbulence, "Detailed Turbulence Reports - Burbank (BUR)", detailed_burbank_dir_png)
    # plot_detailed_turbulence_general(offshore_flow, "Detailed Turbulence Reports - Offshore Flow", detailed_offshore_dir_png)

    # PLOT TURBULENCE 3 YEAR CHUNKS
    plot_turbulence_by_3year_chunks(df, "Turbulence Reports", general_3year_dir_png, False)
    plot_turbulence_by_3year_chunks(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_3year_dir_png, True)
    plot_turbulence_by_3year_chunks(offshore_flow, "Turbulence Reports - Offshore Flow", offshore_3year_dir_png, False)

    # PLOT TURBULENCE FULL Range
    # plot_turbulence_full_range(df, "Turbulence Reports", general_full_dir_png)
    # plot_turbulence_full_range(burbank_turbulence, "Turbulence Reports - Burbank (BUR)", burbank_full_dir_png)
    # plot_turbulence_full_range(offshore_flow, "Turbulence Reports - Offshore Flow", offshore_full_dir_png)
