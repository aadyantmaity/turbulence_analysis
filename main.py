import os
import numpy as np
import pandas as pd
from utils.preprocessing import preprocess_data
from utils.directorycreator import output_dir_svg_spatial_terrain_altitude

input_csv = "pireps_200311300000_202502132359 (1).csv"
output_csvs = {
    'preprocessed': "data_csv_files/preprocessed_dataset.csv",
    'burbank_turbulence': "data_csv_files/burbank_turbulence.csv",
    'burbank_turbulence_severe': "data_csv_files/burbank_turbulence_severe.csv",
    'fl_42000_or_above': "data_csv_files/fl_42000_or_above.csv"
}

df, _ = preprocess_data(input_csv, output_csvs)

if __name__ == "__main__":
    from spatialturbulence import (
        plot_turbulence_for_jan6_to_jan9_google_maps_altitude,
        plot_turbulence_for_dec30_to_jan5_google_maps_altitude,
        plot_turbulence_for_jan6_to_jan9_google_maps_altitude_hourblocks,
    )

    plot_turbulence_for_jan6_to_jan9_google_maps_altitude(
        df, "Turbulence Reports", output_dir_svg_spatial_terrain_altitude)
    plot_turbulence_for_dec30_to_jan5_google_maps_altitude(
        df, "Turbulence Reports", output_dir_svg_spatial_terrain_altitude)
    plot_turbulence_for_jan6_to_jan9_google_maps_altitude_hourblocks(
        df, "Turbulence Reports", output_dir_svg_spatial_terrain_altitude)
